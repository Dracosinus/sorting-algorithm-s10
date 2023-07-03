#!/usr/bin/env python3

from typing import List
from flight import Flight
import all_flights_extractor
from datetime import datetime, time
import copy
from time_helper import divide_mins_to_days_hours_mins


LAST_BUS_DEPART = datetime.fromisoformat('2010-07-27 17:00:00')
FIRST_BUS_ARRIVAL = datetime.fromisoformat('2010-08-03 15:00:00')
PRICE_PER_MINUTE = 5
ALL_FLIGHTS = all_flights_extractor.generate_all_flights()


class Solution(object):
    """A solution is a map of 18 flights containing a ongoing and outgoing flight for each 9 participants

    Args:
        object (List[Flight]): the map to create the object

    Returns:
        Solution: the solution object
    """
    solution_map: List[Flight]
    total_price: int

    def __init__(self,
                 solution_map: List[Flight]) -> None:
        self.solution_map = solution_map
        self.total_price = self.calculate_total_price()

    def to_string(self):
        """displays each of the 18 flights
        """
        for key, flight in self.solution_map.items():
            print(f'For Key : {key}')
            flight.to_string()

    def calculate_total_price(self):
        """Calculates the price of the flight, including time wasters, counting
        - the flight prices
        - a price per minute waited
        - 100 euros more payed if the person waited two hours or more

        Returns:
            float: total price
        """
        total_price = 0
        for flight in self.solution_map.values():
            total_price += flight.price

            if flight.conf_role == 'incoming':
                duration = LAST_BUS_DEPART - flight.arrive
            else:
                duration = flight.depart - FIRST_BUS_ARRIVAL
            difference_in_mins = duration.total_seconds() / 60.0
            waiting_price = difference_in_mins*PRICE_PER_MINUTE
            if difference_in_mins >= 120:
                waiting_price += 100
            total_price += waiting_price

        return total_price

    def calculate_spent_time_in_mins(self):
        """counts the amount of time participants will have waited for both their flights

        Returns:
            float: minutes waited
        """
        spent_time = 0
        for flight in self.solution_map.values():
            if flight.conf_role == 'incoming':
                duration = LAST_BUS_DEPART - flight.arrive
            else:
                duration = flight.depart - FIRST_BUS_ARRIVAL
            difference_in_mins = duration.total_seconds() / 60
            spent_time += difference_in_mins
            # (days, hours, mins) = divide_mins_to_days_hours_mins(difference_in_mins)
            # print(f'we just added {days} days, {hours} hours, {mins} mins')
        return spent_time

    def get_neighbours(self):
        """Every possible neighbours

        Returns:
            List[Solution]
        """
        neighbours = []
        for key, flight in self.solution_map.items():
            flight_list = ALL_FLIGHTS[key]
            index = flight_list.index(flight)
            if index > 0:
                neighbour = copy.copy(self.solution_map)
                neighbour[key] = flight_list[index-1]
                neighbours.append(Solution(neighbour))
            if index+1 < len(flight_list):
                neighbour = copy.copy(self.solution_map)
                neighbour[key] = flight_list[index+1]
                neighbours.append(Solution(neighbour))
        return neighbours

    def find_best_neighbour(self):
        neighbours = self.get_neighbours()
        best_neighbour = self
        best_price = best_neighbour.total_price
        for neighbour in neighbours:
            if neighbour.total_price < best_price:
                best_neighbour = neighbour
                best_price = neighbour.total_price
        return best_neighbour

    def write_report(self):
        print(
            f'Total price for this solution is {self.total_price}')
        duree_minutes = self.calculate_spent_time_in_mins()
        (jours, heures, minutes) = divide_mins_to_days_hours_mins(duree_minutes)
        print(
            f"Attendees will wait {duree_minutes} mins, meaning : {jours} day(s), {heures} hour(s), {minutes} minute(s)")
