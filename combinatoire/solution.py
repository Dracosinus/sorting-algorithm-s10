#!/usr/bin/env python3

from __future__ import annotations
from typing import List, Dict
from datetime import datetime
import copy
from flight import Flight
from flight_extractor import ALL_FLIGHTS

from time_helper import divide_mins_to_days_hours_mins

PRICE_PER_MINUTE = 5

class Solution(object):
    """A solution is a map of 18 flights with both flights for each 9 participants

    Args:
        object (Dict[str, Flight]): the map to create the object

    Returns:
        Solution: the solution object
    """
    solution_map: Dict[str, Flight]
    latest_bus_depart: datetime
    first_bus_arrival: datetime
    total_price: float

    def __init__(self,
                 solution_map: Dict[str, Flight]) -> None:
        self.solution_map = solution_map
        self.latest_bus_depart = self.find_latest_bus_depart()
        self.first_bus_arrival = self.find_first_bus_arrival()
        self.total_price = self.calculate_total_price()

    def to_string(self):
        """displays each of the 18 flights
        """
        for key, flight in self.solution_map.items():
            print(f'For Key : {key}')
            flight.to_string()

    def find_latest_bus_depart(self) -> datetime:
        """returns the last bus depart for the incoming flights

        Returns:
            datetime:
        """
        for flight in self.solution_map.values():
            if flight.conf_role == 'incoming':
                latest_bus_depart = flight.arrive
                break
        for flight in self.solution_map.values():
            if flight.conf_role == 'incoming':
                if flight.arrive > latest_bus_depart:
                    latest_bus_depart = flight.arrive
        return latest_bus_depart

    def find_first_bus_arrival(self) -> datetime:
        """returns the fist bus arrival for the outgoing flights

        Returns:
            datetime:
        """
        for flight in self.solution_map.values():
            if flight.conf_role == 'outgoing':
                first_bus_arrival = flight.depart
                break
        for flight in self.solution_map.values():
            if flight.conf_role == 'outgoing':
                if flight.depart < first_bus_arrival:
                    first_bus_arrival = flight.depart
        return first_bus_arrival

    def calculate_total_price(self) -> float:
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
                duration = self.latest_bus_depart - flight.arrive
            else:
                duration = flight.depart - self.first_bus_arrival
            difference_in_mins = duration.total_seconds() / 60.0
            waiting_price = difference_in_mins*PRICE_PER_MINUTE
            if difference_in_mins >= 120:
                waiting_price += 100
            total_price += waiting_price

        return total_price

    def calculate_spent_time_in_mins(self) -> float:
        """counts the amount of time participants will have waited for both their flights

        Returns:
            float: minutes waited
        """
        spent_time = 0
        for flight in self.solution_map.values():
            if flight.conf_role == 'incoming':
                duration = self.latest_bus_depart - flight.arrive
            else:
                duration = flight.depart - self.first_bus_arrival
            difference_in_mins = duration.total_seconds() / 60
            spent_time += difference_in_mins
            # (days, hours, mins) = divide_mins_to_days_hours_mins(difference_in_mins)
            # print(f'we just added {days} days, {hours} hours, {mins} mins')
        return spent_time
    
    def calculate_dollar_price(self) -> float:
        """sums price of all flights

        Returns:
            float:
        """
        dollar_price = 0
        for flight in self.solution_map.values():
            dollar_price += flight.price
        return dollar_price

    def get_neighbours(self) -> List[Solution]:
        """Every possible neighbours

        Returns:
            List[Solution]
        """
        neighbours = []
        for key, flight in self.solution_map.items():
            flight_list: List[Flight] = ALL_FLIGHTS[key]

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

    def find_best_neighbour(self) -> Solution:
        """the cheapest neighbour

        Returns:
            Solution:
        """
        neighbours = self.get_neighbours()
        best_neighbour = self
        best_price = best_neighbour.total_price
        for neighbour in neighbours:
            if neighbour.total_price < best_price:
                best_neighbour = neighbour
                best_price = neighbour.total_price
        return best_neighbour

    def write_report(self):
        """A report with time spent included
        """
        print(
            f'Solution report \n + Total Price: {self.total_price}\n + Dollar Price: {self.calculate_dollar_price()}')
        duree_minutes = self.calculate_spent_time_in_mins()
        (jours, heures, minutes) = divide_mins_to_days_hours_mins(duree_minutes)
        print(
            f" + Wait time mins: {duree_minutes} \n + Wait time detail: {jours} day(s), {heures} hour(s), {minutes} minute(s)")
