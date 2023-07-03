#!/usr/bin/env python3

from typing import List
from flight import Flight
import all_flights_extractor
from datetime import datetime, time
import copy


LAST_BUS_DEPART = datetime.fromisoformat('2010-07-27 17:00:00')
FIRST_BUS_ARRIVAL = datetime.fromisoformat('2010-08-03 15:00:00')
PRICE_PER_MINUTE = 5
ALL_FLIGHTS = all_flights_extractor.generate_all_flights()


class Solution(object):
    def __init__(self,
                 solution_map: List[Flight]) -> None:
        self.solution_map = solution_map
        self.total_price = self.calculate_total_price()

    def to_string(self):
        for key, flight in self.solution_map.items():
            print(f'For Key : {key}')
            flight.to_string()

    def calculate_total_price(self):
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
        spent_time = 0
        for flight in self.solution_map.values():
            if flight.conf_role == 'incoming':
                duration = LAST_BUS_DEPART - flight.arrive
            else:
                duration = flight.depart - FIRST_BUS_ARRIVAL
            difference_in_mins = duration.total_seconds() / 60.0
            spent_time += difference_in_mins
            # (days, hours, mins) = divide_mins_to_days_hours_mins(difference_in_mins)
            # print(f'we just added {days} days, {hours} hours, {mins} mins')
        return spent_time

    def get_neighbours(self):
        """All possible neighbours of a solution

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
