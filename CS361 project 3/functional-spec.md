# Bend Bike Shop Functional Spec

## Section 1: Write an Overview

The Bend Bike Shop rental system lets customers browse available bikes and locks and reserve them online or at the in-store kiosk, with or without an account. It also gives employees and managers the tools to track rentals, returns, and bikes out for service, process payments and late fees, and view reports on how the business is doing.

## Section 2: Write User Scenarios

Emily is an active long distance bike riding enthusiast who is visiting Bend to see some family while on vacation. She decides she wants to go on a bike ride around Bend to see the sights while she's in town, and because she's already a seasoned bike rider, she decides to browse the Bend Bike Shop catalogue from her cell phone for a road bike. She browses the catalogue and is able to find exactly what she is looking for because the system allows the user to filter the available bikes based on frame size and bike type. She clicks the exact bike she wants, clicks add to reservation, picks her rental time frame, decides to checkout as a guest, fills out her personal details and enters her desired payment method, clicks finalize reservation, arrives on time to the shop and her bike is waiting for her when she gets there. She signs a waiver, goes out and has a good experience seeing everything she wanted to around town, returns her bike on time without any issue, pays her bill with a shop employee’s assistance and goes back to her family to express how much she enjoyed the rental process at the Bend Bike Shop, and ends up leaving a glowing review online because of how smooth and seamless the store's rental system is.

Joe is a service technician working at the Bend Bike Shop. He handles maintenance on the bikes returning from customer use and is the one in charge of final inspection before a bike can be checked back into inventory so the bikes can be rented out again. He is in the process of inspecting a bike and notices one of the sprockets in the gear stack is beginning to rust pretty badly, and decides to flag the bike and make sure it cannot go back out into service until the new sprocket is ordered and replaced so the bike doesn't have any issues when a customer is out riding it. He searches the bike’s serial number to pull up its page, clicks a button that removes the bike from service, enters the reasons into the text field, and saves it in the system. Once the new parts arrive, Joe replaces the worn rusty sprocket, pulls up the bike in the system, adds a comment into the text field saying the rusty worn out sprocket has been replaced, clicks save and clicks a button that moves the bike back into the shop’s available bikes. The system made Joe's job easy to keep track of which bikes are not in service and what repairs are needed for each bike.

Linda has managed the Bend Bike Shop for six years and has learned that August in Bend means one thing: wildfire smoke. She wakes up on a Saturday to an orange sky and an air quality alert, and she knows no one is riding today. She logs into the manager dashboard from her laptop, which shows a live summary of today’s activity: 22 reservations and 0 bikes out. She clicks “Reservations,” filters by today’s date, and sees the full list of customers. She clicks “Select All,” then “Refund / Cancel,” and a confirmation box asks her to enter a reason. She types “Store closed – wildfire smoke” and confirms. The system cancels the reservations without cancellation fees, releases the card pre-authorizations, and records the override and its reason under her manager account. Linda spends the rest of the morning answering exactly zero angry phone calls.

Marcus, a retired schoolteacher, rented a hybrid last summer and liked it enough to make an account. This year he walks up to the in-store kiosk, taps “Log In,” and enters his phone number and password. His home screen shows his past rentals, with a “Rent Again” button next to last year’s hybrid. He taps it, and the system brings up the bike type and size he used before. He picks today, 10am–2pm. On the availability screen, mountain bikes in his size are grayed out for that block, but hybrids are available. He picks one, taps “Add Lock” for a small fee, and moves to checkout. His name, address, phone, and saved card fill in automatically, so he just confirms the payment pre-authorization and taps “Reserve.” The confirmation screen tells him to see an employee at the counter. The employee scans the reservation, hands him the bike, helmet, and lock, and Marcus is out the door in under five minutes.

## Section 3: Write Non-Goals

- Bike and equipment sales (handled by a separate system)
- Outreach or marketing ads (handled by a separate team), and no ads on the kiosk
- Unattended pickups or returns outside business hours; all handoffs and returns go through an employee
- Self-service rental extensions; customers call and an employee decides
- Self-service bike swaps (e.g. wrong size); handled by an employee at the counter
- Automatic charges for lost or stolen bikes; a manager decides what to do
- Automatic discounts based on availability; only date-based discounts set by managers
- Discounts that need verification (e.g. student discounts); handled case-by-case at the counter
- Tracking helmets; they're free, optional, and not tracked
- Tracking locks individually; locks are tracked by count only
- Automatic weather cancellations; managers handle these through the override/refund tools
- Business-side cancellations due to inoperable bikes (tabled for later)
- Limits on how many bikes a customer can reserve; the per-bike cancellation fee covers abuse
- Required customer accounts; guest checkout must always be available
- Automatic customer bans; an employee must ban someone manually
- A built-in waiver system; the kiosk hooks into the existing online waiver
- Building payment or card pre-authorization in-house; handled by an external payment processor API
- Inventory purchasing or bike lifecycle tracking
- An on-premises server; the system will be cloud hosted

## Section 4: Use Case Diagrams

![Use Case Diagram](images/Bend_Bike_Shop_Use_Case_Diagram.png)

## Section 5: UX Flows

Each box is a screen the user sees. Arrows are labeled with the action that takes the user to the next screen.

### Emily – Customer Bike Reservation

![Emily UX Flow](images/Emily_customer_bike_reservation_flowchart.png)

### Joe – Technician Removes and Restores a Bike

![Joe UX Flow](images/Joe_technician_UX_flowchart.png)

### Linda – Manager Cancels the Day's Reservations

![Linda UX Flow](images/Linda_manager_UX_flowchart.png)

## Section 6: Wireframes

**Use case:** Reserve Bike
**Actor:** Customer

These wireframes cover every screen a customer uses to reserve a bike, following Emily's scenario. Emily checks out as a guest; the Login screen covers the sign-in path for returning customers.

### 1. Home Screen

![Home Screen](images/wireframe-01-home.png)

The Home Screen is the first screen a customer sees when visiting the Bend Bike Shop site on their phone. It shows the shop name, a short intro, and basic shop info. Tapping Browse Bikes takes the user to the Bike Catalogue screen, and tapping Sign In takes them to the Login screen.

### 2. Bike Catalogue

![Bike Catalogue](images/wireframe-02-catalogue.png)

The Bike Catalogue screen lists the bikes available to rent, each with a photo, model name, type, frame size, and daily price. The user can filter the list by bike type and frame size, which updates the results on this screen. Tapping View on a bike takes the user to the Bike Details screen, and tapping Home returns to the Home Screen.

### 3. Bike Details

![Bike Details](images/wireframe-03-bike-details.png)

The Bike Details screen shows a larger photo of the selected bike along with its model, type, frame size, daily price, and availability. Tapping Add to Reservation takes the user to the Select Rental Period screen. Tapping Catalogue returns the user to the Bike Catalogue with their filters still applied.

### 4. Select Rental Period

![Select Rental Period](images/wireframe-04-rental-period.png)

The Select Rental Period screen lets the user choose when they will pick up and return the bike. It shows a summary of the selected bike, date and time fields, an availability calendar, and an estimated total that updates as the dates change. Tapping Continue takes the user to the Checkout Options screen.

### 5. Checkout Options

![Checkout Options](images/wireframe-05-checkout-options.png)

The Checkout Options screen shows a summary of the reservation so far (bike, pickup and return times, estimated total) and asks how the user wants to check out. Tapping Checkout as Guest takes the user to the Guest Information screen without creating an account. Tapping Sign In takes returning customers to the Login screen.

### 6. Guest Information

![Guest Information](images/wireframe-06-guest-info.png)

The Guest Information screen collects the contact details the shop needs for a guest reservation: name, email, phone, and an optional height for bike fit. The user fills in the fields and taps Continue to Payment to go to the Payment screen. Tapping Checkout returns the user to the Checkout Options screen.

### 7. Payment

![Payment](images/wireframe-07-payment.png)

The Payment screen lets the user choose a payment method and enter card details, which are pre-authorized to hold the reservation. A note explains that the final bill is settled at the shop on return. Tapping Review Reservation takes the user to the Review Reservation screen, and tapping Your Details returns to the Guest Information screen.

### 8. Review Reservation

![Review Reservation](images/wireframe-08-review.png)

The Review Reservation screen shows everything the user entered (bike, rental period, contact details, payment) so they can check it before committing. Each section has an Edit link that takes the user back to that screen (e.g. Rental Period → Select Rental Period). Checking the terms box and tapping Finalize Reservation submits the reservation and takes the user to the Reservation Confirmation screen.

### 9. Reservation Confirmation

![Reservation Confirmation](images/wireframe-09-confirmation.png)

The Reservation Confirmation screen tells the user their reservation went through and shows the confirmation number, bike, pickup and return times, and the shop's location. It also reminds the user what to bring and that the waiver is signed at pickup. Tapping Back to Home returns the user to the Home Screen.

### 10. Login

![Login](images/wireframe-10-login.png)

The Login screen lets a returning customer sign in with their email and password so their saved contact details are filled in for them. Tapping Sign In & Continue skips the Guest Information screen and takes the user straight to the Payment screen. Tapping Checkout as Guest goes to the Guest Information screen, and tapping Checkout returns to the Checkout Options screen.

## Section 7: Prototype

A working prototype of the Reserve Bike use case (Emily's flow) is in [prototype.html](prototype.html). Download it and open it in a browser to click through the full reservation flow.
