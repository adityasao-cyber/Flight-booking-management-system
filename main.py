"""
Flight Booking Management System
Simple, easy-to-understand console program for booking and managing flights.
"""

import os
import sys
import csv

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLIGHTS_FILE = os.path.join(BASE_DIR, "flights.csv")
BOOKINGS_FILE = os.path.join(BASE_DIR, "bookings.csv")


# =============================================================================
# 1. FLIGHT CLASS
# =============================================================================
class Flight:
    """Stores flight details and manages available seats."""

    def __init__(self, flight_no, origin, destination, seats, fare):
        self.flight_no = str(flight_no).strip().upper()
        self.origin = str(origin).strip()
        self.destination = str(destination).strip()
        self.seats = int(seats)
        self.fare = int(fare)

    def matches_route(self, origin, destination):
        """Checks if flight matches the requested route (case-insensitive)."""
        return (self.origin.lower() == origin.strip().lower() and 
                self.destination.lower() == destination.strip().lower())

    def book_seats(self, num_seats):
        """Reduces seats and returns total fare (seats * fare)."""
        if num_seats < 1:
            raise ValueError("Number of seats must be at least 1.")
        if self.seats == 0:
            raise ValueError(f"Flight {self.flight_no} is full.")
        if num_seats > self.seats:
            raise ValueError(f"Only {self.seats} seat(s) available on {self.flight_no}.")

        self.seats -= num_seats
        return num_seats * self.fare

    def cancel_seats(self, num_seats):
        """Restores cancelled seats back to the flight."""
        self.seats += num_seats
        return self.seats

    def format_search_result(self):
        """Formats flight info for search results."""
        return f"{self.flight_no} | {self.origin} -> {self.destination} | Seats: {self.seats} | Fare: Rs. {self.fare} per seat"


# =============================================================================
# 2. FILE HELPERS (CSV Load & Save)
# =============================================================================
def load_flights():
    """Reads flights from flights.csv into a list of Flight objects."""
    flights = []
    if not os.path.exists(FLIGHTS_FILE):
        return flights

    with open(FLIGHTS_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flights.append(Flight(
                row["FlightNo"], row["Origin"], row["Destination"],
                row["Seats"], row["Fare"]
            ))
    return flights


def save_flights(flights):
    """Saves updated flight seat counts back to flights.csv."""
    with open(FLIGHTS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["FlightNo", "Origin", "Destination", "Seats", "Fare"])
        for f_obj in flights:
            writer.writerow([f_obj.flight_no, f_obj.origin, f_obj.destination, f_obj.seats, f_obj.fare])


def load_bookings():
    """Reads passenger bookings from bookings.csv."""
    bookings = {}
    if not os.path.exists(BOOKINGS_FILE):
        return bookings

    with open(BOOKINGS_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            bid = row["BookingID"].strip().upper()
            bookings[bid] = {
                "BookingID": bid,
                "PassengerName": row["PassengerName"].strip(),
                "FlightNo": row["FlightNo"].strip().upper(),
                "Seats": int(row["Seats"]),
                "TotalFare": int(row["TotalFare"]),
                "Status": row.get("Status", "CONFIRMED").strip().upper()
            }
    return bookings


def save_bookings(bookings):
    """Saves all bookings to bookings.csv."""
    with open(BOOKINGS_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["BookingID", "PassengerName", "FlightNo", "Seats", "TotalFare", "Status"])
        for b in bookings.values():
            writer.writerow([b["BookingID"], b["PassengerName"], b["FlightNo"], b["Seats"], b["TotalFare"], b["Status"]])


# =============================================================================
# 3. CORE ACTIONS (Search, Book, Cancel)
# =============================================================================
def search_flights(flights):
    """Asks for origin & destination, then prints matching flights."""
    print("\n--- Search Flights by Route ---")
    origin = input("Enter Origin City (e.g. Raipur): ").strip()
    destination = input("Enter Destination City (e.g. Delhi): ").strip()

    if not origin or not destination:
        print("[Error] Origin and Destination cannot be empty.")
        return

    matches = [f.format_search_result() for f in flights if f.matches_route(origin, destination)]

    print("\n--- Search Results ---")
    if matches:
        for item in matches:
            print(item)
    else:
        print(f"No flights found from '{origin}' to '{destination}'.")


def book_flight(flights, bookings):
    """Takes passenger details, validates seats, and confirms booking."""
    print("\n--- Book Flight Seats ---")
    flight_no = input("Enter Flight Number (e.g. AI101, AI202): ").strip().upper()
    passenger_name = input("Enter Passenger Name (e.g. Kiran Rao): ").strip()
    seats_str = input("Enter Number of Seats: ").strip()

    # Validate seat count is a positive number
    try:
        num_seats = int(seats_str)
        if num_seats <= 0:
            print("\nNumber of seats must be at least 1.")
            return
    except ValueError:
        print("\n[Error] Invalid seat number. Please provide a positive integer.")
        return

    if not passenger_name:
        print("\n[Error] Passenger name cannot be blank.")
        return

    # Find the flight
    flight = next((f for f in flights if f.flight_no == flight_no), None)
    if not flight:
        print(f"\nFlight {flight_no} not found.")
        return

    # Try booking seats
    try:
        total_fare = flight.book_seats(num_seats)
    except ValueError as err:
        print(f"\n{err}")
        return

    # Create next sequential Booking ID (BK1, BK2, ...)
    highest_id = 0
    for bid in bookings:
        if bid.startswith("BK") and bid[2:].isdigit():
            highest_id = max(highest_id, int(bid[2:]))
    booking_id = f"BK{highest_id + 1}"

    # Save to bookings dictionary
    bookings[booking_id] = {
        "BookingID": booking_id,
        "PassengerName": passenger_name,
        "FlightNo": flight.flight_no,
        "Seats": num_seats,
        "TotalFare": total_fare,
        "Status": "CONFIRMED"
    }

    # Save to files
    save_flights(flights)
    save_bookings(bookings)

    print(f"\nBooking confirmed. ID: {booking_id} | {passenger_name} | {flight.flight_no} | {num_seats} seat(s) | Total: Rs. {total_fare} | Seats left: {flight.seats}")


def cancel_booking(flights, bookings):
    """Cancels an existing booking and restores seats to inventory."""
    print("\n--- Cancel Booking ---")
    booking_id = input("Enter Booking ID to Cancel (e.g. BK1): ").strip().upper()

    if not booking_id:
        print("[Error] Booking ID cannot be blank.")
        return

    if booking_id not in bookings:
        print(f"\nBooking ID {booking_id} not found.")
        return

    booking = bookings[booking_id]

    if booking["Status"] == "CANCELLED":
        print(f"\nBooking {booking_id} is already cancelled.")
        return

    flight = next((f for f in flights if f.flight_no == booking["FlightNo"]), None)
    if not flight:
        print(f"\nAssociated flight {booking['FlightNo']} not found.")
        return

    # Restore seats
    flight.cancel_seats(booking["Seats"])
    booking["Status"] = "CANCELLED"

    # Save to files
    save_flights(flights)
    save_bookings(bookings)

    print(f"\nBooking {booking_id} cancelled. Seats left on {booking['FlightNo']}: {flight.seats}")


def view_flights(flights):
    """Displays flight inventory."""
    print(f"\n--- Current Flight Inventory (Showing first 20 of {len(flights)} flights) ---")
    print(f"{'Flight No':<12} | {'Origin':<16} | {'Destination':<16} | {'Seats':<7} | {'Fare (Rs)':<10}")
    print("-" * 72)
    for f in flights[:20]:
        status_tag = " (FULL)" if f.seats == 0 else ""
        print(f"{f.flight_no:<12} | {f.origin:<16} | {f.destination:<16} | {f.seats:<7} | Rs. {f.fare:<8}{status_tag}")


def view_bookings(bookings):
    """Displays all bookings."""
    print("\n--- Passenger Bookings Ledger ---")
    if not bookings:
        print("No bookings recorded yet.")
        return

    print(f"{'Booking ID':<12} | {'Passenger':<18} | {'Flight':<8} | {'Seats':<6} | {'Total Fare':<12} | {'Status':<10}")
    print("-" * 75)
    for b in bookings.values():
        print(f"{b['BookingID']:<12} | {b['PassengerName']:<18} | {b['FlightNo']:<8} | {b['Seats']:<6} | Rs. {b['TotalFare']:<10} | {b['Status']:<10}")


# =============================================================================
# 4. MAIN MENU LOOP
# =============================================================================
def main():
    flights = load_flights()
    bookings = load_bookings()

    print("=" * 65)
    print("           FLIGHT BOOKING MANAGEMENT SYSTEM")
    print("=" * 65)

    while True:
        print("\n--------------------------- MAIN MENU ---------------------------")
        print("  1. Search Flights by Route (Origin -> Destination)")
        print("  2. Book Flight Seats")
        print("  3. Cancel Booking")
        print("  4. View All Available Flights")
        print("  5. View Booking History & Active Bookings")
        print("  6. Reload / Synchronize Flights Inventory from CSV")
        print("  7. Exit System")
        print("-----------------------------------------------------------------")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            search_flights(flights)
        elif choice == "2":
            book_flight(flights, bookings)
        elif choice == "3":
            cancel_booking(flights, bookings)
        elif choice == "4":
            view_flights(flights)
        elif choice == "5":
            view_bookings(bookings)
        elif choice == "6":
            flights = load_flights()
            bookings = load_bookings()
            print("\n[Success] Flight inventories and bookings synchronized from disk.")
        elif choice == "7":
            print("\n[System] Exiting Flight Booking Management System. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Error] Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
