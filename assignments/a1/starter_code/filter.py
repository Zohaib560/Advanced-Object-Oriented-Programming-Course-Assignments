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
from typing import List
from customer import Customer
from flight import FlightSegment
# from time import sleep


class Filter:
    """ A class for filtering flight segments based on some criterion.

        This is an abstract class. Only subclasses should be instantiated.
    """
    def __init__(self) -> None:
        pass

    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which match the
            filter specified in <filter_string>.

            The <filter_string> is provided by the user through the visual
            prompt, after selecting this filter.

            The <customers> is a list of all customers from the input dataset.

            If the filter has no effect or the <filter_string> is invalid then
            return the same flights segments from the <data> input.

            Precondition:
                - <customers> contains the list of all customers from the input
                  dataset
                - all flight segments included in <data> are valid segments
                  from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """ A class for resetting all previously applied filters, if any. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Reset all of the applied filters. Returns a List containing all the
            flight segments corresponding to all trips of <customers>.

            The <data>, <customers>, and <filter_string> arguments for this
            type of filter are ignored.
        """

        # TODO
        data_list = []
        for customer in customers:
            for trip in customer.get_trips():
                for flight in trip.get_flight_segments():
                    if flight not in data_list:
                        data_list.append(flight)

        return data_list

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Reset all of the filters applied so far (if any)!"


class CustomerFilter(Filter):
    """ A class for selecting the flight segments for a given customer. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> made or received
            by the customer with the id specified in <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            customer ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """

        # TODO
        valid = True
        cus = None

        if len(filter_string) != 6:
            valid = False
        else:
            for char in filter_string:
                if char.isnumeric() is False:
                    valid = False

        if valid:
            cus_id = int(filter_string)
            for customer in customers:
                if customer.get_id() == cus_id:
                    cus = customer
            if cus is None:
                valid = False

        if valid:
            data_c = data.copy()
            cus_f = []
            for trip in cus.get_trips():
                cus_f.extend(trip.get_flight_segments())

            i = 0
            while i < len(data_c):
                if data_c[i] in cus_f:
                    cus_f.remove(data_c[i])
                    i += 1
                elif data_c[i] not in cus_f:
                    data_c.remove(data_c[i])

            return data_c

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """ A class for selecting only the flight segments lasting either over or
        under a specified duration.
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> with a duration of
            under or over the time indicated in the <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "Lxxxx" or "Gxxxx", indicating to filter
            flight segments less than xxxx or greater than xxxx minutes,
            respectively.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """

        # TODO
        valid = True
        if len(filter_string) < 2:
            valid = False
        else:
            if filter_string[0] not in 'GL':
                valid = False
            if valid:
                num = filter_string[1:]
                if num.isnumeric() is False:
                    valid = False

        if valid:
            data_c = data.copy()
            num = int(filter_string[1:])
            i = 0
            if filter_string[0] == 'G':
                while i < len(data_c):
                    time = (data_c[i].get_duration().hour * 60) + \
                           data_c[i].get_duration().minute
                    if time <= num:
                        data_c.remove(data_c[i])
                    elif time > num:
                        i += 1
            elif filter_string[0] == 'L':
                while i < len(data_c):
                    time = (data_c[i].get_duration().hour * 60) + \
                           data_c[i].get_duration().minute
                    if time >= num:
                        data_c.remove(data_c[i])
                    elif time < num:
                        i += 1
            return data_c

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu
        """
        return "Filter flight segments based on duration; " \
               "L#### returns flight segments less than specified length, " \
               "G#### for greater "


class LocationFilter(Filter):
    """ A class for selecting only the flight segments which took place within
        a specific area.
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data>, which took place
            within a location specified by the <filter_string> (the IATA
            departure or arrival airport code of the segment was
            <filter_string>).

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            3-string IATA airport code. In the event of an invalid string:
              1. return the original list <data>, and
              2. your code must not crash.
        """

        # TODO
        valid = True
        if len(filter_string) != 4:
            valid = False
        else:
            if filter_string[0] not in 'DA':
                valid = False
        if valid:
            aid = filter_string[1:]
            for flight in data:
                if flight.get_arr() == aid or flight.get_dep() == aid:
                    valid = True
                    break
                else:
                    valid = False

        if valid:
            data_c = data.copy()
            aid = filter_string[1:]
            i = 0
            if filter_string[0] == 'D':
                while i < len(data_c):
                    if data_c[i].get_dep() != aid:
                        data_c.remove(data_c[i])
                    elif data_c[i].get_dep() == aid:
                        i += 1
            if filter_string[0] == 'A':
                while i < len(data_c):
                    if data_c[i].get_arr() != aid:
                        data_c.remove(data_c[i])
                    elif data_c[i].get_arr() == aid:
                        i += 1
            return data_c

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on an airport location;\n" \
               "DXXX returns flight segments that depart airport XXX,\n"\
               "AXXX returns flight segments that arrive at airport XXX\n"


class DateFilter(Filter):
    """ A class for selecting all flight segments that departed and arrive
    between two dates (i.e. "YYYY-MM-DD/YYYY-MM-DD" or "YYYY MM DD YYYY MM DD").
    """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> that have departed
            and arrived between the range of two dates indicated in the
            <filter_string>.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains the following
            input format: either "YYYY-MM-DD/YYYY-MM-DD" or
            "YYYY MM DD YYYY MM DD", indicating to filter flight segments
            between the first occurrence of YYYY-MM-DD and the second occurence
            of YYYY-MM-DD.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """

        # TODO
        valid = True
        version = 1
        if len(filter_string) != 21:
            valid = False

        if valid:
            d = filter_string
            # version 1 format
            if d[4] != '-' or d[7] != '-' or d[10] != '/' or d[15] != '-' or \
                    d[18] != '-':
                version = 2
                # version 2 format
                if d[4] != ' ' or d[7] != ' ' or d[10] != ' ' or d[15] != ' '\
                        or d[18] != ' ':
                    valid = False

        if valid:
            if version == 1:
                d_start, d_end = filter_string.split('/')
                d_start = d_start.split('-')
                d_end = d_end.split('-')
            elif version == 2:
                date = filter_string.split(' ')
                d_start = date[:3]
                d_end = date[3:]
            try:
                d_start = datetime.date(int(d_start[0]), int(d_start[1]),
                                        int(d_start[2]))
            except ValueError:
                valid = False

            try:
                d_end = datetime.date(int(d_end[0]), int(d_end[1]),
                                      int(d_end[2]))
            except ValueError:
                valid = False

        if valid:
            data_c = data.copy()
            i = 0
            while i < len(data_c):
                if (data_c[i].get_times()[0].date() >= d_start) and \
                        (data_c[i].get_times()[1].date() <= d_end):
                    i += 1
                else:
                    data_c.remove(data_c[i])
            return data_c

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter flight segments based on dates; " \
               "'YYYY-MM-DD/YYYY-MM-DD' or 'YYYY-MM-DD,YYYY-MM-DD'"


class TripFilter(Filter):
    """ A class for selecting the flight segments for a trip. """
    def apply(self, customers: List[Customer], data: List[FlightSegment],
              filter_string: str) -> List[FlightSegment]:
        """ Returns a list of all flight segments from <data> where the
            <filter_string> specified the trip's reservation id.

            The <customers> list contains all customers from the input dataset.

            The filter string is valid if and only if it contains a valid
            Reservation ID.

            If the filter string is invalid, do the following:
              1. return the original list <data>, and
              2. ensure your code does not crash.
        """

        # TODO
        for customer in customers:
            for trip in customer.get_trips():
                if trip.get_reservation_id() == filter_string:
                    return trip.get_flight_segments()

        return data

    def __str__(self) -> str:
        """ Returns a description of this filter to be displayed in the UI menu.
            Unlike other __str__ methods, this one is required!
        """
        return "Filter events based on a reservation ID"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'doctest',
            'customer', 'flight', 'time'
        ],
        'max-nested-blocks': 5,
        'allowed-io': ['apply', '__str__']
    })
