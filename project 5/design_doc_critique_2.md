# Design Doc Critique 2

Three additions the AI made in `design_doc_ai_2.md`, and what I think of each.

## 1. Manager Waiver Override: Breaks What Rodney Wanted

The AI added a `waiver_override_reason` to `check_out_reservation` so a manager can hand off a bike without a signed waiver.  It also uses this as the fix for the "Waiver system is down" failure mode.  In its summary, the AI admits it made this rule up because neither doc says it.

Nothing in the functional spec or design doc says a waiver can be skipped.  Emily signs one at pickup, the confirmation screen reminds customers they'll sign at pickup, and the kiosk exists partly to hook into the shop's existing waiver.  The whole point of a waiver is to protect the shop, so a button that lets someone skip it defeats the purpose.

I'd remove the override.  If the waiver system is down, the handoff waits until the customer signs, or the shop uses a paper waiver and the employee notes it on the reservation.  The system shouldn't decide a rental can go out without a waiver.

## 2. Idempotency Key on create_reservation: Good Idea

The AI added an `idempotency_key` to `create_reservation`.  If the same key comes in twice, the API returns the first reservation instead of creating a second one and placing a second card hold.

I think this is a good addition.  Most customers reserve from their phones like Emily, often on a spotty connection, and it's easy to tap Finalize twice or have the app retry.  Without this, a customer could end up with two reservations and two holds on their card for one bike, and the extra bike is blocked for everyone else.  It's a small change that prevents a real, annoying problem.

## 3. Extending a Rental: I'd Do It Differently

The AI added `extend_reservation` so an employee can extend a rental when a customer calls.  When it does, it recalculates `total_cents` for the whole rental at today's prices and discounts, not just the extra time.

That means extending a rental can change what the customer already agreed to pay for the original time.  If a manager has raised the lock fee or removed the discount they booked with, adding two hours would charge them the new prices for the time they already booked.  It also goes against the AI's own "price is fixed at booking" invariant, which it gets around by adding an exception just for extensions.

I'd keep the original `total_cents` as is and only price the added time, at today's rates, then add it to the total.  The customer keeps the price they were quoted, and the extra time is charged fairly.
