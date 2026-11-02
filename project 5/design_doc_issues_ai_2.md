
# Design Doc Review: Bend Bike Shop Technical Design Doc

**Scope:** The doc is partial and its sections are examples, so I haven't counted missing interfaces, invariants or failure modes as issues.  The items below are contradictions, gaps and structural problems in what's already there.  Line numbers refer to the uploaded file.

---

## 1. Logical Issues (High Priority)

### 1.1 Late fees can exceed the pre-auth hold
- `calculate_rental_price` is the pre-auth amount and leaves out late fees (L247).  `check_in_reservation` captures the final total *including* late fees (L270).
- Most processors won't capture more than the authorized amount.  `PaymentGateway` (L192–198) only has `capture(preauthId, ...)`.  There's no way to charge an amount above the hold.
- **Fix:** Pre-auth with a buffer, or add a separate `charge(cardToken, amount)` path for the overage.

### 1.2 Guests can't be re-authorized or charged later
- Guests have `card_token = null` (L119), and `RESERVATION` stores only `preauth_id` (L131).  After a guest reservation, nothing keeps a card token.
- Three things need one and can't get it for guests: re-authorizing 24 hours before pickup (L312), "staff can charge it later" for unpaid returns (L311), and the overage charge in 1.1.
- The fix for an expired hold says to "email the customer to update their card" (L312).  No flow lets a guest do that.

### 1.3 Cancellation fees "charged at return"
- The Goal says cards are "charged at return, including late fees and cancellation fees" (L22).  A cancelled reservation never has a return.
- The cancellation fee is never defined anywhere: no amount, no cutoff window, no field, no interface.  A Non-Goal still relies on it to "cover abuse" (L45).

### 1.4 No-shows aren't handled
- Nothing covers a customer who never picks up.  The reservation stays `RESERVED` forever, the bike stays blocked, and the hold just ends up expiring.
- There's no grace period, no auto-cancel and no no-show fee.

### 1.5 Check-in skips the technician's inspection
- The Service Technician "inspects returned bikes" (L13).  `check_in_reservation` sets bikes straight back to `AVAILABLE` (L270), so a damaged bike can be rented again before anyone looks at it.
- Back-to-back reservations are allowed with no turnaround buffer (L232–233), which makes this worse.

### 1.6 The caller supplies the return time
- `check_in_reservation` takes `returned_at` as a parameter (L265).  Any logged-in staff member could backdate it and wipe out a late fee, and nothing records that it happened.  That runs against the "overrides are recorded" invariant (L305).
- **Fix:** Use server time, or require a manager override with a reason.

### 1.7 The "next-day service" assumption doesn't match search behavior
- The assumption says a bike out for service will be available by the next day (L64).  `search_available_bikes` never returns an `OUT_OF_SERVICE` bike for *any* date range (L233), so a bike in for a quick tune-up today disappears from next week's searches.
- The assumption is also unsafe as written, and `set_bike_service_status` already plans for bikes that won't be ready in time (L285).
- Either use the assumption in availability logic and state that, or drop it.

### 1.8 Bike status has no state machine
- `BikeStatus` (`AVAILABLE` / `RENTED` / `OUT_OF_SERVICE`) duplicates what reservations already say, and the two can disagree:
  - `set_bike_service_status(in_service=true)` sets `AVAILABLE` even if the bike is currently `RENTED` (L283).
  - `check_in_reservation` sets `AVAILABLE` even if someone marked the bike out of service during the rental (L270).
- **Fix:** Define allowed transitions, or derive `RENTED` from reservations.

### 1.9 Reminder retries conflict with the reminder NFR
- The NFR says reminders go out within 5 minutes of each mark (L74).  The failure mode retries for up to 1 hour (L313).  A late-retried "1 hour before" reminder could land at or after the due time and overlap the next reminder.
- "Confirmation numbers are shown on screen" (L313) helps with confirmations only, not with reminders.

### 1.10 The all-or-nothing guarantee spans an external system
- `create_reservation` promises "all or nothing" (L259), but the pre-auth is an external call.  If the pre-auth succeeds and the DB commit then fails, a hold is left orphaned.  A release step needs to be spelled out.
- The race-condition fix ("re-check and save inside one database transaction," L314) is only correct with serializable isolation or row/range locking.  A read-check-write inside a default READ COMMITTED transaction can still double-book.  Making the external pre-auth call inside that transaction also holds locks for the length of a network call.

### 1.11 Local time with no UTC offset is ambiguous across DST
- `DateTime` is defined as Pacific local time (L211).  During the fall-back hour, times like 1:30 AM happen twice, and block pricing across a DST change is ambiguous.
- **Fix:** Store UTC and display in Pacific.

---

## 2. Data Model Can't Support the Rest of the Doc

Some of these may just be because the doc is partial.  They're listed because other sections already depend on them.

| Referenced elsewhere | Problem in the data model |
|---|---|
| Invariant 4: overrides recorded with staff ID and reason (L305) | `RESERVATION` has no fields for cancelling staff, reason or refunds.  `Reservation.cancel(byManager: bool, reason)` (L179) takes a bool, not a staff ID, so it can't satisfy the invariant. |
| "Flagged as unpaid" / "flagged for follow-up" (L270, L296, L311) | There's no flag field, and `ReservationStatus` has no matching value. |
| Bans "by name and phone" (L12); Database lists "bans" (L96) | There's only `CUSTOMER.is_banned`.  If guests get a new `CUSTOMER` row per reservation, a banned person can just check out again as a guest.  The doc never says how `create_reservation` (which takes `ContactInfo`) matches a ban. |
| Staff accounts and roles (L96) | No `STAFF` entity.  `SERVICE_NOTE.staff_id` (L145) isn't a foreign key to anything. |
| Lock counts (L42, L96) | No lock inventory, and no check anywhere that `lock_count` ≤ locks available. |
| Discounts (L96, L245) | No discount entity. |
| Waiver confirmed by an employee before handoff (L93) | No waiver status field.  The Staff Dashboard has no connection to the Waiver system (L87), so the doc doesn't show how the employee confirms it. |
| `RESERVATION }o--|{ BIKE` (L110) | A many-to-many relationship with no junction table. |
| Guest and account holder rows in one `CUSTOMER` table (L105) | Email/phone uniqueness isn't specified.  Account login probably needs a unique email, but repeat guests will reuse emails. |

---

## 3. Interface Issues

- **`Requires` and `Outcomes` overlap:** `create_reservation` *requires* that bikes are available and the customer isn't banned (L257), then lists those same cases as handled errors under Outcomes (L258).  Pick one: either they're preconditions (and the caller's responsibility) or they're defined error outcomes.
- **Pricing terms are undefined** (L245):
  - "12-hour rate": bikes only have `block_rate_cents` (per 4 hours).  Is the 12-hour rate 3 blocks?  Does a "day" mean business hours or 24 hours?
  - The lock fee has no amount and nowhere to be stored.
  - The late fee rule isn't defined anywhere in the doc.
  - The discount applies "on the pickup date" only.  It's unclear whether that's intended for multi-day rentals.
- **"Same inputs on the same day always give the same price"** (L246): if a manager edits discounts mid-day, this is false.  The doc also doesn't say whether the final charge at return uses the price stored at reservation (`total_cents`) or a recalculated one.
- **Business hours aren't defined**, even though `search_available_bikes` requires them (L231).  The maximum advance-booking window isn't defined either, and it matters for hold expiry (L312).  The doc also doesn't require `pickup_time` to be in the future.
- **`create_reservation` can't tell guests from account holders:** there's no `customer_id` or session context in the signature (L252), yet account details are "filled in from the account" (L260).
- **Confirmation sending isn't covered by the atomicity guarantee:** the doc doesn't say whether an SMS/email failure rolls back the reservation.  It shouldn't, and the doc should say so.
- **`staff_id` is passed as a parameter** (L265, L277, L290) even though the API "handles role checks" (L207).  It should come from the authenticated session, or a caller could claim to be any staff member.
- **Multi-bike reservations allow only whole returns:** there's no partial return or one-bike-late case.
- **`bulk_cancel_reservations`:**
  - Customer notification is in Notes (L298), but it's a behavior, so it belongs in Outcomes.
  - If one ID isn't `RESERVED`, the doc doesn't say whether the whole call fails or skips that ID.
  - "Linda's smoke day" (L294) refers to context the reader doesn't have.
- **`refund(preauthId, ...)`** (L197): refunds usually reference a capture or charge ID, which isn't stored anywhere.
- **`set_bike_service_status`:** when the flagged bike has no available swap, the only option is a business-side cancellation, which is tabled as a Non-Goal (L44).

---

## 4. Component and Diagram Consistency

- The Backend API mentions scheduled jobs for return reminders only (L95).  The hold re-auth job (L312) and notification retries (L313) are missing.
- In the class diagram, `Reservation` lacks `totalCents` and any customer reference, though both are in the ERD and the interface record.
- `Bike.isAvailable(start, end)` (L188) depends on reservation data, so it's an odd responsibility for `Bike`.
- `Customer.ban()` (L164) bans a customer record, but bans are described as by name and phone (L12).  Section 2 covers the mismatch.

---

## 5. Structural Issues

- **The same point is repeated across sections:**
  - "Guest checkout always available" appears in Goals (L21), Non-Goals (L46) and Constraints (L58).
  - Cloud hosting appears in Non-Goals (L51) and Constraints (L55).
  - The external payment processor appears in Non-Goals (L49) and Constraints (L56).
  - The existing waiver appears in Non-Goals (L48) and Constraints (L57).
  - Pick one home for each.  Non-Goals should list things the system won't do, not restate requirements in negative form.
- **A requirement is listed as a Non-Goal:** "no ads on the kiosk" (L34) is a constraint.
- **A fact is listed as an Assumption:** "At most 60 bikes are out at once, since the fleet is 60 bikes" (L63) is true by definition and assumes nothing.  If fleet size matters, put it in Overview or Constraints.
- **Goals don't cover the Actors:** employee check-in/out and manual bans are in Actors (L12) but have no Goal.  Technician inspection (L13) also has no Goal.
- **Actors vs. interface:** Actors say the technician removes bikes from service (L13), but the interface lets any employee do it (L285).  It's not a contradiction, but Actors should say so.
- **Waivers per rider:** one reservation can cover several bikes and riders.  The doc doesn't say whether each rider needs a waiver.

---

## 6. Minor

- Extra blank lines before the H1 (L1–3).
- There's no upper bound on keeping customer contact data (L75 sets only a minimum).  That's worth stating for privacy.
- The doc doesn't say whether `confirmation_number` is unique, or how it's generated.