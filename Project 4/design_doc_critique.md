
# Design Doc Critique

Three additions the AI made in design_doc_ai.md, and critiques for each.

## 1. Pricing Table: Breaks What Rodney Wanted

The AI's pricing rule is daily_rate × rental days, with any partial day counted as one day, and it lists hourly pricing as an open question.

Rodney already answered this.  He rents in 4-hour blocks, a day's fee equals 12 hours, and rentals max out at 7 days.  
Under the AI's rule, Marcus's 10am–2pm rental gets charged a full day, which is about triple what Rodney's model would charge for one 4-hour block.
The AI also never enforces the 7-day limit anywhere.

The rule should be price by 4-hour block, cap each day at the 12-hour rate, and reject any rental longer than 7 days.

## 2. Roles and Permissions Table: I'd Do It Differently

The AI only lets Technician and above add service notes and remove or restore bikes.  
That means a regular employee at the counter can't mark a bike out for repair.

Rodney said employees should be able to mark bikes in, out, or out for repair.  I'd give employees and technicians the same permissions and treat "technician" as a job title instead of a separate role.  
That matches how my Actors section already describes technicians "an employee who inspects returned bikes", and it keeps the role list to what Rodney asked for - owner, manager, employee.

## 3. Double-Booking Prevention: Good Idea

In Availability Rules, the AI re-checks availability inside a database transaction and locks the selected bike rows before creating the reservation.  
If someone else grabbed the bike first, the API returns 409 Conflict and the app sends the customer back to pick another bike.

I think this is a good addition.  Customers can book from the web and the kiosk at the same time, so two people could try to reserve the last hybrid in the same second.  
Without this, both could get a confirmation for the same bike, and one of them shows up to nothing.  
Since all handoffs go through an employee, that would turn into an awkward conversation at the counter.  This should prevent that from happening.