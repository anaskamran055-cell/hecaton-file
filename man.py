# ===============================================================
# SMART BUS TICKET BOOKING & RESERVATION SYSTEM
# Python 3 console application (sirf built-in Python, in-memory data)
# ===============================================================

# ---------------- STEP 1: DATA ----------------

# Saare routes: list of dictionaries
routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad",
     "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur",
     "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas",
     "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore",
     "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad",
     "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30},
]

bookings = []        # saari bookings (cancelled bhi)
booking_ids = set()  # ab tak issue hui booking IDs (duplicate rokne ke liye)
cities = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")  # fixed cities


# ---------------- HELPER FUNCTIONS ----------------

def find_route(route_id):
    """Route ID se route dhundo. Na mile to None wapas karo."""
    for route in routes:
        if route["route_id"] == route_id:
            return route
    return None


def seat_status(route):
    """Route ki seat status text wapas karta hai."""
    if route["available_seats"] == 0:
        return "Fully Booked"
    elif route["available_seats"] == route["total_seats"]:
        return "Available"
    else:
        return "Partially Booked"


def generate_booking_id():
    """Aisi booking ID banao jo set mein pehle se na ho."""
    number = 1001
    while "B" + str(number) in booking_ids:
        number += 1
    new_id = "B" + str(number)
    booking_ids.add(new_id)
    return new_id


def read_positive_int(message):
    """Positive integer lo. Galat ho to None wapas karo (crash nahi hoga)."""
    text = input(message).strip()
    try:
        value = int(text)
    except ValueError:
        return None
    if value <= 0:
        return None
    return value


# ---------------- FEATURE 3: VIEW ROUTES ----------------

def view_routes():
    choice = input("Sirf available routes dekhni hain? (y/n): ").strip().lower()
    only_available = (choice == "y")

    print("\nAVAILABLE BUS ROUTES")
    print(f"{'No.':<4} {'Route':<6} {'Journey':<28} {'Depart':<9} {'Fare':<9} Seats")
    for index, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue  # full route skip karo
        journey = route["departure_city"] + " -> " + route["destination_city"]
        fare = "Rs." + str(route["ticket_price"])
        if route["available_seats"] == 0:
            seats = "Fully Booked"
        else:
            seats = str(route["available_seats"]) + "/" + str(route["total_seats"])
        print(f"{index:<4} {route['route_id']:<6} {journey:<28} "
              f"{route['departure_time']:<9} {fare:<9} {seats}")

    show_schedule = input("\nDeparture city ke hisab se schedule dekhna hai? (y/n): ").strip().lower()
    if show_schedule == "y":
        view_schedule()


# ---------------- FEATURE 10: SCHEDULE ----------------

def view_schedule():
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city in cities:                      # bahar wala loop: cities
        print(city)
        has_departure = False
        for route in routes:                 # andar wala loop: routes
            if route["departure_city"] == city:
                print("   ", route["route_id"], "->", route["destination_city"],
                      "|", route["departure_time"])
                has_departure = True
        if not has_departure:
            print("    No scheduled departures.")


# ---------------- FEATURE 4: SEARCH ----------------

def search_route():
    term = input("Search by route ID or city: ").strip().lower()
    if term == "":
        print("Kuch to likho search ke liye.")
        return

    found = False
    for route in routes:
        if term == route["route_id"].lower():
            # route ID unique hoti hai, isliye match milte hi ruk jao
            print(route["route_id"], "|", route["departure_city"], "->",
                  route["destination_city"], "| Rs.", route["ticket_price"], "|",
                  route["available_seats"], "seats available")
            found = True
            break
        elif term == route["departure_city"].lower() or term == route["destination_city"].lower():
            # city search mein saare matches dikhao
            print(route["route_id"], "|", route["departure_city"], "->",
                  route["destination_city"], "| Rs.", route["ticket_price"], "|",
                  route["available_seats"], "seats available")
            found = True
    else:
        # loop bina break ke khatam hua
        if not found:
            print("No matching route found.")


# ---------------- FEATURE 5: BOOK A TICKET ----------------

def book_ticket():
    print("\n--- BOOK A TICKET ---")

    # 1) Naam
    name = input("Passenger name: ").strip()
    if name == "":
        print("Error: Naam khali nahi ho sakta.")
        return

    # 2) Age
    age = read_positive_int("Passenger age: ")
    if age is None:
        print("Error: Age positive number honi chahiye.")
        return

    # 3) Route
    route_id = input("Route ID (e.g. R101): ").strip().upper()
    route = find_route(route_id)
    if route is None:
        print("Error: Ye route exist nahi karta.")
        return

    # 4) Seats
    seats = read_positive_int("Number of seats: ")
    if seats is None:
        print("Error: Seats 0 se zyada integer honi chahiye.")
        return

    # 5) Availability
    if seats > route["available_seats"]:
        print("Error: Sirf", route["available_seats"], "seats available hain.")
        return

    # Sab checks pass: ab hi record banao aur seats kam karo
    booking_id = generate_booking_id()
    total_fare = route["ticket_price"] * seats

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed"
    }
    bookings.append(booking)
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print("Booking ID:", booking_id)
    print("Passenger:", name)
    print("Route:", route_id, "(" + route["departure_city"], "->", route["destination_city"] + ")")
    print("Seats booked:", seats)
    print("Fare per seat: Rs.", route["ticket_price"])
    print("Total fare: Rs.", total_fare)
    print("Status: Confirmed")


# ---------------- FEATURE 6: VIEW BOOKINGS ----------------

def view_bookings():
    if len(bookings) == 0:
        print("No bookings found.")
        return

    print("\nMY BOOKINGS")
    for index, booking in enumerate(bookings, start=1):
        route = find_route(booking["route_id"])
        journey = route["departure_city"] + " -> " + route["destination_city"]
        print(f"{index}. {booking['booking_id']} | {booking['passenger_name']} | "
              f"{booking['route_id']} ({journey}) | Seats: {booking['seats']} | "
              f"Fare: Rs. {booking['total_fare']} | {booking['status']}")


# ---------------- FEATURE 7: CANCEL BOOKING ----------------

def cancel_booking():
    booking_id = input("Enter booking ID to cancel: ").strip().upper()

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["status"] == "Confirmed":
                route = find_route(booking["route_id"])
                route["available_seats"] += booking["seats"]   # seats wapas (sirf ek baar)
                booking["status"] = "Cancelled"                # record delete nahi, status badla
                print("Booking", booking_id, "has been cancelled.")
                print("Seats restored:", booking["seats"])
                print("Route", route["route_id"], "available seats:", route["available_seats"])
            else:
                print("Error: Ye booking pehle hi cancel ho chuki hai.")
            break
    else:
        print("Error: Booking ID nahi mili.")


# ---------------- FEATURE 8: SEAT AVAILABILITY ----------------

def view_availability():
    choice = input("Sirf seats wale routes dekhne hain? (y/n): ").strip().lower()
    only_available = (choice == "y")

    print("\nSEAT AVAILABILITY")
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue
        print(route["route_id"], "|", route["departure_city"], "->", route["destination_city"],
              "|", route["available_seats"], "/", route["total_seats"], "|", seat_status(route))


# ---------------- FEATURE 9: REPORT ----------------

def generate_report():
    total_bookings = len(bookings)
    confirmed_count = 0
    cancelled_count = 0

    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed_count += 1
        elif booking["status"] == "Cancelled":
            cancelled_count += 1

    reserved_seats = 0
    confirmed_revenue = 0
    fully_booked_routes = 0

    # nested loop: har route ke liye uski confirmed bookings
    for route in routes:
        if route["available_seats"] == 0:
            fully_booked_routes += 1
        for booking in bookings:
            if booking["route_id"] == route["route_id"] and booking["status"] == "Confirmed":
                reserved_seats += booking["seats"]
                confirmed_revenue += booking["total_fare"]

    print("\nBOOKING REPORT")
    print("Total bookings created:", total_bookings)
    print("Confirmed bookings:", confirmed_count)
    print("Cancelled bookings:", cancelled_count)
    print("Seats currently reserved:", reserved_seats)
    print(f"Confirmed revenue: Rs. {confirmed_revenue:,}")
    print("Fully booked routes:", fully_booked_routes)


# ---------------- STEP 2: MAIN MENU ----------------

def show_menu():
    print("\nSMART BUS RESERVATION SYSTEM")
    print("================================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("================================")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if not choice.isdigit():
            print("Error: Please number likho (1-8).")
            continue

        choice = int(choice)

        if choice == 1:
            view_routes()
        elif choice == 2:
            search_route()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("Thank you! Goodbye.")
            break
        else:
            print("Error: Choice 1 se 8 ke beech honi chahiye.")


main()
