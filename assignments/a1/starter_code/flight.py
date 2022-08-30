"""
UTM:CSC148, Winter 2020
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Bogdan Simion, Michael Liut, Paul Vrbik
"""
from __future__ import annotations
from typing import Dict, List, Optional, Tuple
import datetime

# Global Airplane Seat Type capacity
AIRPLANE_CAPACITY = {"Economy": 150, "Business": 22}


class FlightSegment:
    """ A FlightSegment offered by the airline system.

    === Public Attributes ===
    seat_capacity:
        the class of seat and total number of seats available on a specific
        segment.
    seat_availability:
        the class of seat and number of seats still available on a specific
        segment.

    === Representation Invariants ===
        -  the keys in seat_availability.keys() must all be >= 0
           (i.e. they cannot be negative)
    """

    # === Private Attributes ===
    # _flight_id:
    #     a unique identifier for this flight.
    # _time:
    #     a tuple containing the departure and arrival time of a segment.
    # _manifest:
    #      a list of tuples containing all customers' ID and type of flight
    #      class that they've taken (e.g. economy).
    # _base_fare_cost:
    #     the base cost of the fare (e.g., $0.1225/km).
    # _flight_duration:
    #     the total time it takes for the flight segment to complete.
    # _flight_length:
    #     the number of kilometres between the departure and arrival locations.
    # _dep_loc:
    #     the unique 3-digit (IATA) airport identifier of where the flight
    #     segment is departing (i.e. leaving from).
    # _arr_loc:
    #     the unique 3-digit (IATA) airport identifier of where the flight
    #     segment is landing (i.e. arriving to).
    # _long_lat:
    #     a tuple of tuples, containing the longitude and latitude of the
    #     departure and arrival destinations.
    #
    # === Representation Invariants ===
    #     -  _flight_length >= 0
    #     -  _dep_loc and _arr_loc must be exactly three characters [A-Z]
    #        and are assumed to be valid and distinct IATA airport codes.

    seat_capacity: Dict[str, int]  # str: class, int: seats_available
    seat_availability: Dict[str, int]  # str: class, int: seats_available
    _flight_id: str
    _time: Tuple[datetime.datetime, datetime.datetime]
    _base_fare_cost: float
    _flight_duration: datetime.time
    _flight_length: float
    _dep_loc: str
    _arr_loc: str
    _long_lat: Tuple[Tuple[float, float], Tuple[float, float]]
    _manifest: List[Tuple[int, str]]  # (customer_id, seat_type)

    def __init__(self, fid: str, dep: datetime.datetime, arr: datetime.datetime,
                 base_cost: float, length: float, dep_loc: str, arr_loc: str,
                 long_lat: Tuple[Tuple[float, float],
                                 Tuple[float, float]]) -> None:
        """ Initialize a FlightSegment object based on the parameters specified.
        """

        self._flight_id = fid
        self._base_fare_cost = base_cost
        self.seat_capacity = AIRPLANE_CAPACITY.copy()
        self.seat_availability = self.seat_capacity.copy()
        self._time = (dep, arr)
        s = (arr - dep).total_seconds()
        h = s // (60 * 60)
        m = ((s / 60) - (h * 60))
        h, m = int(h), round(m)
        self._flight_duration = datetime.time(h, m)
        self._flight_length = length
        self._dep_loc = dep_loc
        self._arr_loc = arr_loc
        self._long_lat = long_lat
        self._manifest = []

    def __repr__(self) -> str:
        return ("[" + str(self._flight_id) + "]:" + str(self._dep_loc) + "->" +
                str(self._arr_loc))

    def get_length(self) -> float:
        """ Returns the length, in KMs, of this flight segment. """

        return self._flight_length

    def get_times(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """ Returns the (departure, arrival) time of this flight segment. """

        # TODO
        return self._time

    def get_arr(self) -> str:
        """ Returns the arrival airport (i.e. the IATA). """

        # TODO
        return self._arr_loc

    def get_dep(self) -> str:
        """ Returns the departure airport (i.e. the IATA). """

        # TODO
        return self._dep_loc

    def get_fid(self) -> str:
        """ Returns the flight identifier. """

        # TODO
        return self._flight_id

    def get_long_lat(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """ Returns the longitude and latitude of a FlightSegment,
            specifically like this: ((LON1, LAT1), (LON2, LAT2)).
        """

        # TODO
        return self._long_lat

    def get_duration(self) -> datetime.time:
        """ Returns the duration of the flight. """

        # TODO
        return self._flight_duration

    def get_base_fare_cost(self) -> float:
        """ Returns the base fare cost for this flight segment. """

        # TODO
        return self._base_fare_cost

    def check_manifest(self, cid: int) -> bool:
        """ Returns True if a certain customer <cid> has booked a seat
            on this specific flight, otherwise False.
        """

        # TODO
        for customer in self._manifest:
            if customer[0] == cid:
                return True
        return False

    def check_seat_class(self, cid: int) -> Optional[str]:
        """ Checks the manifest to see what class of cabin a certain customer
            (based on their <cid>) has booked. None is returned in the event
            there is no seat booked for that <cid>.
        """

        # TODO
        for customer in self._manifest:
            if customer[0] == cid:
                return customer[1]
        return None

    def book_seat(self, cid: int, seat_type: str) -> None:
        """ Book a seat of the given <seat_type> for the customer <cid>.
            If that customer is already booked, do nothing. If the seat
            type is different, and it is available, make the change.
        """

        # TODO
        if (cid, seat_type) in self._manifest:
            return None
        for customer in self._manifest:
            if customer[0] == cid:
                if customer[1] != seat_type and \
                        self.seat_availability[customer[1]] > 0:
                    seat = customer[1]
                    self._manifest.remove(customer)
                    self.seat_availability[seat] += 1
                    self._manifest.append((cid, seat_type))
                    self.seat_availability[seat_type] -= 1
                return None
        self._manifest.append((cid, seat_type))
        return None

    def cancel_seat(self, cid: int) -> None:
        """	If a seat has already been booked by <cid>, cancel the booking
            and restore the seat's availability. Otherwise, do nothing and
            return None.
        """

        # TODO
        for customer in self._manifest:
            if customer[0] == cid:
                seat = customer[1]
                self._manifest.remove(customer)
                self.seat_availability[seat] += 1
                return None
        return None


# ------------------------------------------------------------------------------
class Trip:
    """ A Trip is composed of FlightSegment(s) which makes up a customer's
        itinerary.

    === Public Attributes ===
    reservation_id:
         a unique identifier for this trip.
    customer_id:
         the unique identifier of the customer who booked this trip.
    trip_departure:
         the date in which this trip was booked.
    """
    # === Private Attributes ===
    # _flights:
    #      a list of all flight segments for this particular trip
    reservation_id: str
    customer_id: int
    trip_departure: datetime.date
    _flights: List[FlightSegment]

    def __init__(self, rid: str, cid: int, trip_date: datetime.date,
                 flight_segments: List[FlightSegment]) -> None:
        """ Initializes a trip object given the specified parameters. """

        # TODO
        self.reservation_id = rid
        self.customer_id = cid
        self.trip_departure = trip_date
        self._flights = flight_segments

    def get_flight_segments(self) -> List[FlightSegment]:
        """ Returns a list of all Flight Segments part of this booking. """

        # TODO
        return self._flights

    def get_reservation_id(self) -> str:
        """ Returns this Trip's Reservation ID. """

        # TODO
        return self.reservation_id

    def get_in_flight_time(self) -> int:
        """ Returns the amount of time (in minutes) the trip is spent in
            flight (i.e. the time in the air only).
        """

        # TODO
        time = 0
        segments = self.get_flight_segments()
        for flight in segments:
            h = flight.get_duration().hour
            m = flight.get_duration().minute
            flight_time = (h * 60) + m
            flight_time = flight_time
            time += flight_time
        time = int(time)
        return time

    def get_total_trip_time(self) -> int:
        """ Returns the amount of time (in minutes) the trip is takes,
            including all transit time (i.e. including waiting for the next
            flight on a layover).
        """

        # TODO
        segments = self.get_flight_segments()
        if len(segments) == 0:
            return 0
        else:
            first_flight_time = segments[0].get_times()[0]
            last_flight_time = segments[0].get_times()[1]
            for flight in segments:
                if flight.get_times()[0] < first_flight_time:
                    first_flight_time = flight.get_times()[0]
                if flight.get_times()[1] > last_flight_time:
                    last_flight_time = flight.get_times()[1]
            total_time = last_flight_time - first_flight_time
            time = total_time.total_seconds()
            time = round(time / 60)
            time = int(time)
        return time


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'doctest',
            'datetime', '__future__'
        ],
        'max-attributes': 11,
        'max-args': 9
    })
