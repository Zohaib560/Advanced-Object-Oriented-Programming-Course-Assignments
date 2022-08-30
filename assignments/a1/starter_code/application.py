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
import datetime
import csv
from typing import Dict, List, Tuple, Optional
from airport import Airport
from customer import Customer
from flight import Trip, FlightSegment
from visualizer import Visualizer

#############################################
# DO NOT DECLARE ANY OTHER GLOBAL VARIABLES!
#############################################

# AIRPORT_LOCATIONS: global mapping of an airport's IATA with their respective
#                    longitude and latitude positions.
# NOTE: This is used for our testing purposes, so it has to be populated in
# create_airports(), but you are welcome to use it as you see fit.
AIRPORT_LOCATIONS = {}

# DEFAULT_BASE_COST: Default rate per km for the base cost of a flight segment.
DEFAULT_BASE_COST = 0.1225


def import_data(file_airports: str, file_customers: str, file_segments: str,
                file_trips: str) -> Tuple[List[List[str]], List[List[str]],
                                          List[List[str]], List[List[str]]]:
    """ Opens all the data files <data/filename.csv> which stores the CSV data,
        and returns a tuple of lists of lists of strings. This contains the read
        in data, line-by-line, (airports, customers, flights, trips).

        Precondition: the dataset file must be in CSV format.
    """

    airport_log, customer_log, flight_log, trip_log = [], [], [], []

    airport_data = csv.reader(open(file_airports))
    customer_data = csv.reader(open(file_customers))
    flight_data = csv.reader(open(file_segments))
    trip_data = csv.reader(open(file_trips))

    for row in airport_data:
        airport_log.append(row)

    for row in flight_data:
        flight_log.append(row)

    for row in customer_data:
        customer_log.append(row)

    for row in trip_data:
        trip_log.append(row)

    return airport_log, flight_log, customer_log, trip_log


def create_customers(log: List[List[str]]) -> Dict[int, Customer]:
    """ Returns a dictionary of Customer IDs and their Customer instances, based
    on the customers from the input dataset from the <log>.

    Precondition:
        - The <log> list contains the input data in the correct format.
    """

    # TODO
    customers_dict = {}
    for c in log:  # c represents a customer
        cus_id, name, age, nat = int(c[0]), c[1], int(c[2]), c[3]
        new_c = Customer(cus_id, name, age, nat)
        customers_dict[cus_id] = new_c
    return customers_dict


def create_flight_segments(log: List[List[str]])\
        -> Dict[datetime.date, List[FlightSegment]]:
    """ Returns a dictionary storing all FlightSegments, indexed by their
    departure date, based on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """

    # TODO
    flight_dict = {}
    for f in log:
        fid, dep_loc, arr_loc, d, dep_t, arr_t, length = f[0], f[1], f[2], \
                                                         f[3], f[4], f[5], \
                                                         float(f[6])
        d, dep_t, arr_t = d.split(":"), dep_t.split(":"), arr_t.split(":")
        flight_date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
        dep_date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]),
                                     int(dep_t[0]), int(dep_t[1]))
        if datetime.time(int(arr_t[0]), int(arr_t[1])) <= \
                datetime.time(int(dep_t[0]), int(dep_t[1])):
            x = flight_date + datetime.timedelta(1)
            arr_date = datetime.datetime(x.year, x.month, x.day, int(arr_t[0]),
                                         int(arr_t[1]))
        else:
            arr_date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]),
                                         int(arr_t[0]), int(arr_t[1]))
        # long_lat = (AIRPORT_LOCATIONS[dep_loc], AIRPORT_LOCATIONS[arr_loc])
        new_flight = FlightSegment(fid, dep_date, arr_date, DEFAULT_BASE_COST,
                                   length, dep_loc, arr_loc,
                                   (AIRPORT_LOCATIONS[dep_loc],
                                    AIRPORT_LOCATIONS[arr_loc]))
        if flight_date in flight_dict:
            flight_dict[flight_date].append(new_flight)
        else:
            flight_dict[flight_date] = [new_flight]
    return flight_dict


def create_airports(log: List[List[str]]) -> List[Airport]:
    """ Return a list of Airports with all applicable data, based
    on the input dataset stored in the <log>.

    Precondition:
    - The <log> list contains the input data in the correct format.
    """

    # TODO
    airports_lst = []
    for airport in log:
        aid, name, location = airport[0], airport[1], (float(airport[2]),
                                                       float(airport[3]))
        new_airport = Airport(aid, name, location)
        airports_lst.append(new_airport)
        if aid not in AIRPORT_LOCATIONS:
            AIRPORT_LOCATIONS[aid] = location
    return airports_lst


def load_trips(log: List[List[str]], customer_dict: Dict[int, Customer],
               flight_segments: Dict[datetime.date, List[FlightSegment]]) \
        -> List[Trip]:
    """ Creates the Trip objects and makes the bookings.

    Preconditions:
    - The <log> list contains the input data in the correct format.
    - the customers are already correctly stored in the <customer_dict>,
    indexed by their customer ID.
    - the flight segments are already correctly stored in the <flight_segments>,
    indexed by their departure date
    """

    # TODO
    trip_list = []
    for trip in log:
        curr_datetime = datetime.datetime(int(trip[2].split('-')[0]),
                                          int(trip[2].split('-')[1]),
                                          int(trip[2].split('-')[2]), 0, 0)
        curr_day = datetime.date(int(trip[2].split('-')[0]),
                                 int(trip[2].split('-')[1]),
                                 int(trip[2].split('-')[2]))
        flight_segs = []
        if trip[0] != 'None':
            total_flights = trip[3:]
            flight_data = []

            for i in range(0, len(total_flights), 2):
                flight_data.append((total_flights[i].strip("''([])"),
                                    total_flights[i + 1].strip("''([])")))

            if int(trip[1]) in customer_dict:
                customer = customer_dict[int(trip[1])]
                if len(customer.get_trips()) > 0:
                    latest_fly = customer.get_trips()[-1].get_flight_segments()
                    for flight in latest_fly:
                        if flight.get_times()[1] > curr_datetime:
                            curr_datetime = flight.get_times()[1]

                _load_trip_helper(curr_day, curr_datetime, flight_data,
                                  flight_segs, flight_segments)

            if None not in flight_segs:
                trip_list.append(customer_dict[int(trip[1])].book_trip
                                 (trip[0], flight_segs, datetime.date(
                                     int(trip[2].split('-')[0]),
                                     int(trip[2].split('-')[1]),
                                     int(trip[2].split('-')[2]))))

    return trip_list


def _load_trip_helper(curr_day: datetime.date, curr_datetime: datetime.datetime,
                      flight_data: list, flight_segs: list,
                      flight_segments:
                      Dict[datetime.date, List[FlightSegment]]) -> None:
    """ This is a helper function for load_trips and is not meant to be used
    as a standalone function.
    
    """

    for i in range(len(flight_data) - 1):
        best_flight = None
        available = False

        while (curr_day <= max(flight_segments)) and available is not \
                True:
            if curr_day in flight_segments:
                for flight in flight_segments[curr_day]:
                    if flight.get_arr() == flight_data[i + 1][0] and \
                            flight.get_dep() == flight_data[i][0] and \
                            flight.seat_availability[flight_data[i][1]] > 0 and\
                            (curr_datetime <= flight.get_times()[0]):
                        available = True
                        best_flight = flight
            curr_day = curr_day + datetime.timedelta(1)
        curr_day = curr_day - datetime.timedelta(1)

        if (curr_day <= max(flight_segments)) and best_flight is not \
                None:
            for flight in flight_segments[curr_day]:
                if flight.get_arr() == flight_data[i + 1][0] and \
                        flight.get_dep() == flight_data[i][0] and \
                        flight.seat_availability[flight_data[i][1]] > 0 and \
                        (curr_datetime <= flight.get_times()[0] <=
                         best_flight.get_times()[0]):
                    best_flight = flight

        if best_flight is None:
            flight_segs.append(best_flight)
            break
        else:
            curr_datetime = best_flight.get_times()[1]
            flight_segs.append((best_flight, flight_data[i][1]))


if __name__ == '__main__':
    print("\n---------------------------------------------")
    print("Reading in all data! Processing...")
    print("---------------------------------------------\n")

    # input_data = import_data('data/airports.csv', 'data/customers.csv',
    #     'data/segments.csv', 'data/trips.csv')

    input_data = import_data('data/airports.csv', 'data/customers.csv',
                             'data/segments_small.csv', 'data/trips_small.csv')

    airports = create_airports(input_data[0])
    print("Airports Created! Still Processing...")
    flights = create_flight_segments(input_data[1])
    print("Flight Segments Created! Still Processing...")
    customers = create_customers(input_data[2])
    print("Customers Created! Still Processing...")
    print("Loading trips can take a while...")
    trips = load_trips(input_data[3], customers, flights)
    print("Trips Created! Opening Visualizer...\n")

    flights_len = 0
    for ky in flights:
        flights_len += len(flights[ky])

    print("---------------------------------------------")
    print("Some Statistics:")
    print("---------------------------------------------")
    print("Total airports in the dataset:", len(airports))
    print("Total flight segments in the dataset:", flights_len)
    print("Total customers in the dataset:", len(customers))
    print("Total trips in the dataset:", len(trips))
    print("---------------------------------------------\n")

    all_flights = [seg for tp in trips for seg in tp.get_flight_segments()]
    all_customers = [customers[cid] for cid in customers]

    V = Visualizer()
    V.draw(all_flights)

    while not V.has_quit():

        flights = V.handle_window_events(all_customers, all_flights)

        all_flights = []

        for flt in flights:
            all_flights.append(flt)

        V.draw(all_flights)

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'csv', 'datetime', 'doctest',
            'visualizer', 'customer', 'flight', 'airport'
        ],
        'max-nested-blocks': 6,
        'allowed-io': [
            'create_customers', 'create_airports', 'import_data',
            'create_flight_segments', 'load_trips'
        ],
        'generated-members': 'pygame.*'
    })
