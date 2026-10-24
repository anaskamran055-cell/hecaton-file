# SmartBus – Bus Ticket Booking & Reservation System

A bus ticket booking system built in two versions that share the same logic:

1. **Console app** (`bus_booking.py`): a Python 3 menu-driven program that runs in the terminal.
2. **Website** (`bus-booking.html`): a responsive, single-file website with the same features, a hero banner, and a photo gallery for your own buses.

Both versions keep data **in memory only**. Nothing is saved after the program or page is closed (see [Limitations](#limitations) and [Roadmap](#roadmap)).

---

## Features

| Feature | Console | Website |
|---|---|---|
| View all routes with fare, departure time and seats | Yes | Yes |
| Filter to routes that still have seats | Yes | Yes |
| Search by route ID or city | Yes | Yes (partial matches work) |
| Book a ticket with full input validation | Yes | Yes |
| View bookings | Yes | Yes |
| Cancel a booking (seats are restored once) | Yes | Yes |
| Seat availability with status labels | Yes | Yes (in the routes table) |
| Booking report (counts, seats, revenue) | Yes | Yes (live-updating) |
| Schedule grouped by departure city | Yes | No |
| Upload your own bus photos | No | Yes |

### Seat status labels

- **Available**: no seats booked on the route.
- **Partially Booked**: some seats taken, some left.
- **Fully Booked**: no seats left. The route cannot be booked.

### Validation rules

- Passenger name cannot be empty.
- Age must be a whole number greater than 0.
- Route must exist.
- Seats must be a whole number greater than 0 and cannot exceed the available seats.
- A booking that is already cancelled cannot be cancelled again.

Cancelled bookings are never deleted. Their status changes to `Cancelled`, so reports and history stay accurate.

---

## Project structure

```
.
├── bus_booking.py      # Python console application
├── bus-booking.html    # Single-file website (HTML + CSS + JavaScript)
└── README.md
```

---

## Getting started

### Console app

Requirements: Python 3.8 or newer. No external packages are needed.

```bash
python bus_booking.py
```

You will see this menu:

```
1. View Available Routes
2. Search for a Route
3. Book a Ticket
4. View My Bookings
5. Cancel a Booking
6. View Seat Availability
7. Generate Booking Report
8. Exit
```

### Website

No build step and no server are needed. Open `bus-booking.html` in any modern browser.

To add your own bus photos, go to the **Our buses** section and click a tile. Choose an image from your device and it replaces the placeholder. Photos added this way last only until the page is reloaded. To make them permanent, embed them in the HTML file.

---

## Data model

### Route

| Field | Description |
|---|---|
| `route_id` | Unique ID such as `R101` |
| `departure_city` | Starting city |
| `destination_city` | Final city |
| `departure_time` | Departure time, for example `08:00 AM` |
| `ticket_price` | Price per seat in Rs. |
| `total_seats` | Seat capacity of the bus |
| `available_seats` | Seats still free |

### Booking

| Field | Description |
|---|---|
| `booking_id` | Unique ID such as `B1001` |
| `passenger_name` | Name of the passenger |
| `passenger_age` | Age of the passenger |
| `route_id` | Route that was booked |
| `seats` | Number of seats booked |
| `total_fare` | `ticket_price × seats` |
| `status` | `Confirmed` or `Cancelled` |

### Default routes

| ID | Journey | Departs | Fare (Rs.) | Seats |
|---|---|---|---|---|
| R101 | Karachi to Hyderabad | 08:00 AM | 1,200 | 40 |
| R102 | Karachi to Sukkur | 09:30 AM | 2,000 | 36 |
| R103 | Hyderabad to Mirpur Khas | 11:00 AM | 800 | 32 |
| R104 | Karachi to Lahore | 07:00 PM | 5,000 | 45 |
| R105 | Sukkur to Hyderabad | 02:00 PM | 1,500 | 30 |

---

## Limitations

- **No persistence.** All routes, bookings and seat counts are lost when the program closes or the page reloads.
- **No shared state.** In the website version, each visitor has their own separate copy of the data. Two people can book the same seat because there is no central server.
- **No authentication, payments or notifications.**

These are fine for learning and demos, but not for a real bus company with many customers.

---

## Roadmap

To serve many users, add a backend and a database:

```
Website (browser)  →  Backend API  →  Database
```

1. **Backend API** (for example FastAPI or Flask in Python) that validates bookings and reduces seats on the server. Seat counting must happen on the server so that two people cannot book the last seat at the same time.
2. **Database** (PostgreSQL, MySQL, or a hosted service such as Supabase or Firebase) with `routes` and `bookings` tables matching the data model above.
3. **Admin login** so only staff can manage routes and view reports.
4. **Online payments** (for example JazzCash, Easypaisa or card) processed on the server.
5. **SMS or email confirmation** after each booking.
6. **HTTPS and data protection.** Passenger details are personal data and must be stored and transmitted securely.

---

## License

Add a license of your choice (for example MIT) before publishing this project.# hecaton-file
