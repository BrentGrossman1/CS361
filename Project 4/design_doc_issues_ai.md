# Design Doc Issues Report

## Summary

The document is well organized and all sections required for this phase are present.  Most issues are consistency gaps between sections, a few assumptions that don't hold up, and pieces missing from the component diagram and table.

---

## Logical Issues

### 1. Service Technician missing from role-based access
- **Where:** Actors, Constraints, Component Table
- **Issue:** Actors lists Service Technician, but the role-based access constraint only names owner, manager, and employee.  The Staff & Manager Dashboard description also says employees mark bikes out for service, which Actors assigns to technicians.
- **Fix:** Add Service Technician to the constraint, state its permissions, and align the dashboard description with who actually removes/restores bikes.

### 2. Pre-authorization timing is underspecified
- **Where:** Goals, Assumptions
- **Issue:** Cards are pre-authorized at reservation and charged at return.  Card holds typically expire after a set number of days, so a reservation made well in advance may lose its hold before pickup.  Late fees can also exceed the pre-authorized amount.
- **Fix:** Add an assumption or constraint covering hold duration (e.g., pre-auth placed at reservation or re-placed X days before pickup) and how charges above the held amount are handled.

### 3. "Saved cards" vs. "never stores card numbers"
- **Where:** Goals, Constraints
- **Issue:** Account holders get saved cards, but the system never stores card numbers.  Not contradictory, but the mechanism isn't stated.
- **Fix:** Clarify that saved cards are payment processor tokens, and list tokens in the Database description.

### 4. Service-time assumption hides an unhandled case
- **Where:** Assumptions, Non-Goals
- **Issue:** The doc assumes a bike out for service is available by the next day, and separately tables business-side cancellations for inoperable bikes.  Together, a bike can be shown as available tomorrow, reserved, and still be broken, with no defined handling.
- **Fix:** Either keep service bikes unavailable until a technician restores them, or explicitly call this out as a known risk tied to the tabled non-goal.

### 5. Peak load reasoning is flawed
- **Where:** Assumptions, Non-Functional Requirements
- **Issue:** "60 rentals a day because the fleet is 60 bikes" assumes each bike rents once per day; short rentals could turn bikes over multiple times.  System load is also driven more by browsing traffic than completed rentals, and the 50-concurrent-user NFR isn't connected to this assumption.
- **Fix:** Reword as max concurrent rentals = 60, and base the concurrent user figure on expected browsing traffic.

### 6. Uptime only covers business hours, but online reservations don't
- **Where:** Non-Functional Requirements
- **Issue:** Customers can reserve online at any time, but the uptime target only applies during business hours.  "Business hours" is also never defined.
- **Fix:** Define business hours and either extend the target to the customer web app 24/7 or accept lower availability off-hours explicitly.

### 7. Banning guests
- **Where:** Actors, Non-Goals
- **Issue:** Employees can ban customers, but guest checkout is always available.  There's no stated way to identify a banned guest (phone, email, card token, etc.).
- **Fix:** State what identifier a ban is tied to and add bans to the Database description.

### 8. Waiver status isn't visible to the system
- **Where:** Constraints, Component Diagram, Component Table
- **Issue:** The Kiosk App description says it provides a link to the online waiver, and the Backend API has no connection to the waiver system.  The system can't confirm a waiver is signed before handoff, and it's unclear how web app customers sign at all.
- **Fix:** State where online customers sign (e.g., at pickup via kiosk) and how staff verify it, either through an API connection to the waiver system or a manual check by the employee at handoff.

---

## Structural Issues

### 9. Components missing from the diagram
- **Issue:** A few pieces implied by the goals don't appear:
  - **Scheduler / background jobs:** Return reminders and the reminder timing NFR need a timed process, not just request-driven API calls.
  - **Authentication / role management:** Accounts and role-based access need a home.
  - **Payment processor callbacks:** Arrows only go from the API outward; processor webhooks (auth expired, charge failed) aren't shown.
- **Fix:** Add a scheduler/worker component and an auth component (or note in the table that they live inside the Backend API), and show return arrows where external systems call back.

### 10. Database description is incomplete
- **Issue:** The table lists bikes, reservations, customers, accounts, and rental history.  Other data the goals depend on isn't listed: lock counts, service status and notes, bans, discounts, staff accounts and roles, payment tokens, and recorded reasons for bulk cancels/refunds.
- **Fix:** Expand the description, or note that it's a summary and the full data model comes in a later section.

### 11. Dashboard name doesn't reflect all users
- **Issue:** "Staff & Manager Dashboard" is also used by technicians and the owner.
- **Fix:** Rename (e.g., "Staff Dashboard") or note in the table who uses it.

### 12. Non-Goals duplicate Constraints
- **Issue:** Required accounts, in-house payments, built-in waiver, and on-prem server appear in both Non-Goals and Constraints.
- **Fix:** Keep them in Constraints and trim from Non-Goals, or keep both if intentional for emphasis.

---

## Minor Issues

### 13. Features in Actors but not in Goals
- Managers set date-based discounts and manage employees; the owner manages managers.  Neither discounts nor user management appears in Goals.

### 14. NFR measurability
- "Pages load in under 2 seconds" should specify a percentile (e.g., 95th percentile).
- "99.5% uptime" should specify a measurement window (e.g., monthly).

### 15. Reminder edge case
- For rentals shorter than an hour, the 1-hour-before reminder would fire before pickup.  Define behavior (skip it, or send at pickup).

### 16. Guest contact info
- Reminders and confirmations go out by SMS/email, but nothing states that guest checkout requires a phone number or email.

### 17. Customer Web App label mismatch
- The diagram labels it "(phone)" while the table says "mobile-friendly site."  Use one consistent description.

### 18. Confirmations not in Goals
- The SMS/Email Service sends confirmations, but only return reminders appear in Goals.

### 19. Cancellation fee undefined
- The per-bike cancellation fee is referenced as the abuse control, but when it applies (cancellation window) isn't defined anywhere in this doc.