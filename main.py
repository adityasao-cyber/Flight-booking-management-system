"""
Flight Booking Management System
A clean and easy-to-understand console application for flight search, seat booking, and cancellations.
"""

import os
import sys
import csv
from datetime import datetime

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FLIGHTS_FILE = os.path.join(BASE_DIR, "flights.csv")
BOOKINGS_FILE = os.path.join(BASE_DIR, "bookings.csv")


# =============================================================================
# 1. FLIGHT CLASS
# =============================================================================
class Flight:
    """Represents a single flight with its details and seat inventory."""

    def __init__(self, flight_no, origin, destination, seats, fare):
        self.flight_no = str(flight_no).strip().upper()
        self.origin = str(origin).strip()
        self.destination = str(destination).strip()
        self.seats = int(seats)
        self.fare = int(fare)

    def matches_route(self, origin, destination):
        """Case-insensitive check for departure and arrival cities."""
        return (self.origin.lower() == origin.strip().lower() and 
                self.destination.lower() == destination.strip().lower())

    def book_seats(self, num_seats):
        """Deducts seats and returns the total fare."""
        if num_seats < 1:
            raise ValueError("Number of seats must be at least 1.")
        if self.seats == 0:
            raise ValueError(f"Flight {self.flight_no} is full.")
        if num_seats > self.seats:
            raise ValueError(f"Only {self.seats} seat(s) available on {self.flight_no}.")

        self.seats -= num_seats
        return num_seats * self.fare

    def cancel_seats(self, num_seats):
        """Restores seats back to available inventory."""
        self.seats += num_seats
        return self.seats

    def format_search_result(self):
        """Returns formatted string for route search results."""
        return f"{self.flight_no} | {self.origin} -> {self.destination} | Seats: {self.seats} | Fare: Rs. {self.fare} per seat"

    def __str__(self):
        return self.format_search_result()


# =============================================================================
# 2. BOOKING CLASS
# =============================================================================
class Booking:
    """Represents a passenger flight reservation."""

    def __init__(self, booking_id, passenger_name, flight_no, seats, total_fare, timestamp=None, status="CONFIRMED"):
        self.booking_id = str(booking_id).strip().upper()
        self.passenger_name = str(passenger_name).strip()
        self.flight_no = str(flight_no).strip().upper()
        self.seats = int(seats)
        self.total_fare = int(total_fare)
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = str(status).strip().upper()

    def format_confirmation(self, seats_left):
        """Returns standard booking confirmation message."""
        return (f"Booking confirmed. ID: {self.booking_id} | {self.passenger_name} | "
                f"{self.flight_no} | {self.seats} seat(s) | Total: Rs. {self.total_fare} | Seats left: {seats_left}")


# =============================================================================
# 3. SERVICE LAYER (Data Persistence & Business Logic)
# =============================================================================
class FlightBookingService:
    """Manages flight inventory and booking transactions."""

    def __init__(self, flights_file=FLIGHTS_FILE, bookings_file=BOOKINGS_FILE):
        self.flights_file = flights_file
        self.bookings_file = bookings_file
        self.flights = []
        self.bookings = {}
        self.reload()

    def load_flights(self):
        """Reads flights from CSV."""
        self.flights = []
        if not os.path.exists(self.flights_file):
            return
        with open(self.flights_file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.flights.append(Flight(
                    row["FlightNo"], row["Origin"], row["Destination"],
                    row["Seats"], row["Fare"]
                ))

    def save_flights(self):
        """Writes current flights back to CSV."""
        with open(self.flights_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["FlightNo", "Origin", "Destination", "Seats", "Fare"])
            for f_obj in self.flights:
                writer.writerow([f_obj.flight_no, f_obj.origin, f_obj.destination, f_obj.seats, f_obj.fare])

    def load_bookings(self):
        """Reads bookings from CSV."""
        self.bookings = {}
        if not os.path.exists(self.bookings_file):
            return
        with open(self.bookings_file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                bid = row["BookingID"].strip().upper()
                self.bookings[bid] = Booking(
                    booking_id=bid,
                    passenger_name=row["PassengerName"],
                    flight_no=row["FlightNo"],
                    seats=row["Seats"],
                    total_fare=row["TotalFare"],
                    timestamp=row.get("Timestamp", ""),
                    status=row.get("Status", "CONFIRMED")
                )

    def save_bookings(self):
        """Writes all bookings to CSV."""
        with open(self.bookings_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["BookingID", "PassengerName", "FlightNo", "Seats", "TotalFare", "Timestamp", "Status"])
            for b in self.bookings.values():
                writer.writerow([b.booking_id, b.passenger_name, b.flight_no, b.seats, b.total_fare, b.timestamp, b.status])

    def reload(self):
        """Reloads both flights and bookings from files."""
        self.load_flights()
        self.load_bookings()

    def _get_next_booking_id(self):
        """Generates the next sequential booking ID (BK1, BK2, etc.)."""
        highest = 0
        for bid in self.bookings:
            if bid.startswith("BK") and bid[2:].isdigit():
                highest = max(highest, int(bid[2:]))
        return f"BK{highest + 1}"

    def find_flight(self, flight_no):
        """Finds a flight by flight number."""
        target = flight_no.strip().upper()
        for f in self.flights:
            if f.flight_no == target:
                return f
        return None

    def search_flights(self, origin, destination):
        """Returns list of formatted strings for flights matching route."""
        return [f.format_search_result() for f in self.flights if f.matches_route(origin, destination)]

    def book_flight(self, flight_no, passenger_name, num_seats):
        """Validates and books seats on a flight."""
        if num_seats < 1:
            return False, "Number of seats must be at least 1."

        clean_name = passenger_name.strip()
        if not clean_name:
            return False, "Passenger name cannot be blank."

        flight = self.find_flight(flight_no)
        if not flight:
            return False, f"Flight {flight_no.strip().upper()} not found."

        try:
            total_fare = flight.book_seats(num_seats)
        except ValueError as err:
            return False, str(err)

        booking_id = self._get_next_booking_id()
        booking = Booking(booking_id, clean_name, flight.flight_no, num_seats, total_fare)
        self.bookings[booking_id] = booking

        self.save_flights()
        self.save_bookings()

        return True, booking.format_confirmation(seats_left=flight.seats)

    def cancel_booking(self, booking_id):
        """Cancels a booking and restores seat count."""
        clean_id = booking_id.strip().upper()
        booking = self.bookings.get(clean_id)

        if not booking:
            return False, f"Booking ID {booking_id} not found."

        if booking.status == "CANCELLED":
            return False, f"Booking {clean_id} is already cancelled."

        flight = self.find_flight(booking.flight_no)
        if not flight:
            return False, f"Associated flight {booking.flight_no} not found."

        flight.cancel_seats(booking.seats)
        booking.status = "CANCELLED"

        self.save_flights()
        self.save_bookings()

        return True, f"Booking {clean_id} cancelled. Seats left on {booking.flight_no}: {flight.seats}"


# =============================================================================
# 4. COMMAND LINE INTERFACE (CLI)
# =============================================================================
class FlightBookingCLI:
    """Handles user input and menu interactions."""

    def __init__(self):
        self.service = FlightBookingService()

    def run(self):
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
                self.handle_search()
            elif choice == "2":
                self.handle_booking()
            elif choice == "3":
                self.handle_cancellation()
            elif choice == "4":
                self.handle_view_flights()
            elif choice == "5":
                self.handle_view_bookings()
            elif choice == "6":
                self.service.reload()
                print("\n[Success] Flight inventories and bookings synchronized from disk.")
            elif choice == "7":
                print("\n[System] Exiting Flight Booking Management System. Goodbye!")
                sys.exit(0)
            else:
                print("\n[Error] Invalid choice. Please enter a number between 1 and 7.")

    def handle_search(self):
        print("\n--- Search Flights by Route ---")
        origin = input("Enter Origin City (e.g. Raipur): ").strip()
        destination = input("Enter Destination City (e.g. Delhi): ").strip()

        if not origin or not destination:
            print("[Error] Origin and Destination cannot be empty.")
            return

        results = self.service.search_flights(origin, destination)
        print("\n--- Search Results ---")
        if results:
            for r in results:
                print(r)
        else:
            print(f"No flights found from '{origin}' to '{destination}'.")

    def handle_booking(self):
        print("\n--- Book Flight Seats ---")
        flight_no = input("Enter Flight Number (e.g. AI101, AI202): ").strip()
        passenger_name = input("Enter Passenger Name (e.g. Kiran Rao): ").strip()
        seats_str = input("Enter Number of Seats: ").strip()

        try:
            num_seats = int(seats_str)
            if num_seats <= 0:
                print("\nNumber of seats must be at least 1.")
                return
        except ValueError:
            print("\n[Error] Invalid seat number. Please provide a positive integer.")
            return

        success, message = self.service.book_flight(flight_no, passenger_name, num_seats)
        print("\n" + message)

    def handle_cancellation(self):
        print("\n--- Cancel Booking ---")
        booking_id = input("Enter Booking ID to Cancel (e.g. BK1): ").strip()
        if not booking_id:
            print("[Error] Booking ID cannot be blank.")
            return

        success, message = self.service.cancel_booking(booking_id)
        print("\n" + message)

    def handle_view_flights(self):
        total = len(self.service.flights)
        print(f"\n--- Current Flight Inventory ({total} total flights) ---")
        page_size = 20
        total_pages = (total + page_size - 1) // page_size
        current_page = 1

        while True:
            start_idx = (current_page - 1) * page_size
            end_idx = min(start_idx + page_size, total)
            page_flights = self.service.flights[start_idx:end_idx]

            print(f"\nPage {current_page} of {total_pages} (Flights {start_idx + 1} to {end_idx}):")
            print(f"{'Flight No':<12} | {'Origin':<16} | {'Destination':<16} | {'Seats':<7} | {'Fare (Rs)':<10}")
            print("-" * 72)
            for f in page_flights:
                status_tag = " (FULL)" if f.seats == 0 else ""
                print(f"{f.flight_no:<12} | {f.origin:<16} | {f.destination:<16} | {f.seats:<7} | Rs. {f.fare:<8}{status_tag}")

            if current_page >= total_pages:
                print("\n[End of inventory reached.]")
                break

            prompt = input(f"\n[Press Enter for next page ({current_page + 1}/{total_pages}), 'a' for all, or 'q' to return to menu]: ").strip().lower()
            if prompt in ('q', 'quit', 'exit'):
                break
            elif prompt in ('a', 'all'):
                for f in self.service.flights[end_idx:]:
                    status_tag = " (FULL)" if f.seats == 0 else ""
                    print(f"{f.flight_no:<12} | {f.origin:<16} | {f.destination:<16} | {f.seats:<7} | Rs. {f.fare:<8}{status_tag}")
                break
            else:
                current_page += 1

    def handle_view_bookings(self):
        print("\n--- Passenger Bookings Ledger ---")
        if not self.service.bookings:
            print("No bookings recorded yet.")
            return

        print(f"{'Booking ID':<12} | {'Passenger':<18} | {'Flight':<8} | {'Seats':<6} | {'Total Fare':<12} | {'Status':<10}")
        print("-" * 75)
        for b in self.service.bookings.values():
            print(f"{b.booking_id:<12} | {b.passenger_name:<18} | {b.flight_no:<8} | {b.seats:<6} | Rs. {b.total_fare:<10} | {b.status:<10}")


if __name__ == "__main__":
    cli = FlightBookingCLI()
    cli.run()
