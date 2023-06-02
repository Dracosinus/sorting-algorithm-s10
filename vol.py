#!/usr/bin/python3

import xml.etree.ElementTree as ET
import os
import random
import copy
from datetime import datetime

LAST_BUS_DEPART = datetime.fromisoformat('2010-07-27 17:00:00')
FIRST_BUS_ARRIVAL = datetime.fromisoformat('2010-08-03 15:00:00')


class Flight:
    def __init__(self, price, stops, orig, dest, depart, arrive, airline_display, conf_role):
        self.price = price
        self.stops = stops
        self.orig = orig
        self.dest = dest
        self.depart = depart
        self.arrive = arrive
        self.airline_display = airline_display
        self.conf_role = conf_role

    @classmethod
    def from_xml_element(cls, element):
        price = float(element.find('price').text)
        stops = element.find('stops').text
        orig = element.find('orig').text
        dest = element.find('dest').text
        depart = datetime.fromisoformat(element.find('depart').text)
        arrive = datetime.fromisoformat(element.find('arrive').text)
        airline_display = element.find('airline_display').text

        return cls(price, stops, orig, dest, depart, arrive, airline_display, 'incoming')

# def load_flights_from_xml(filename):
#     flights = []
#     tree = ET.parse(filename)
#     root = tree.getroot()

#     for flight_element in root.findall('flight'):
#         flight = Flight.from_xml_element(flight_element)
#         flights.append(flight)

#     return flights


def load_flights_from_xml(filename):
    flights = []
    tree = ET.parse(filename)
    root = tree.getroot()

    for flight_element in root.findall('flight'):
        flight = Flight.from_xml_element(flight_element)
        if '08-03' in filename or '08-04' in filename:
            flight.conf_role = 'outgoing'
            if flight.depart >= FIRST_BUS_ARRIVAL:
                flights.append(flight)
        else:
            if flight.arrive <= LAST_BUS_DEPART:
                flights.append(flight)
    return flights


def find_all_flights_in_directory(directory):
    cheapest_flights = {}

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            all_flights = load_flights_from_xml(filepath)
            key = os.path.splitext(filename)[0]
            cheapest_flights[key] = all_flights

    return cheapest_flights


def merge_flights(flights1, flights2):
    merged_flights = {}

    # Merge flights from the first dictionary
    for key, flights in flights1.items():
        merged_flights[key] = flights

    # Merge flights from the second dictionary
    for key, flights in flights2.items():
        if key in merged_flights:
            merged_flights[key].extend(flights)
        else:
            merged_flights[key] = flights

    return merged_flights


def print_flight(flight):
    print('Price:', flight.price)
    print('Stops:', flight.stops)
    print('Origin:', flight.orig)
    print('Destination:', flight.dest)
    print('Departure:', flight.depart)
    print('Arrival:', flight.arrive)
    print('Airline:', flight.airline_display)
    print('ConfRole:', flight.conf_role)
    print('---')


def get_random_solution(flights):
    solution = {}
    for key, flights_list in flights.items():
        solution[key] = random.choice(flights_list)
    return solution


def print_solution(solution):
    for key, flight in solution.items():
        print(f'For Key : {key}')
        print_flight(flight)


def calculate_total_price(solution):
    total_price = 0
    for flights in solution.values():
        total_price += flights.price
    return total_price


def get_neighbours(solution, all_flights):
    neighbours = []
    for key, flight in solution.items():
        flight_list = all_flights[key]
        index = flight_list.index(flight)
        if index > 0:
            neighbour = copy.copy(solution)
            neighbour[key] = flight_list[index-1]
            neighbours.append(neighbour)
        if index+1 < len(flight_list):
            neighbour = copy.copy(solution)
            neighbour[key] = flight_list[index+1]
            neighbours.append(neighbour)
    return neighbours

def find_best_neighbour(solution, neighbours):
    best_neighbour=solution
    best_price=calculate_total_price(best_neighbour)
    for neighbour in neighbours:
        if calculate_total_price(neighbour) < best_price:
            best_neighbour=neighbour
            best_price=calculate_total_price(neighbour)
    return best_neighbour
        

def generate_all_flights():
    directory_0726 = 'ThirdParty/FlightData/2010/07-26/'
    cheapest_flights_0726 = find_all_flights_in_directory(directory_0726)

    directory_0727 = 'ThirdParty/FlightData/2010/07-27/'
    cheapest_flights_0727 = find_all_flights_in_directory(directory_0727)
    ongoing_flights = merge_flights(
        cheapest_flights_0726, cheapest_flights_0727)

    directory_0803 = 'ThirdParty/FlightData/2010/08-03/'
    cheapest_flights_0803 = find_all_flights_in_directory(directory_0803)

    directory_0804 = 'ThirdParty/FlightData/2010/08-04/'
    cheapest_flights_0804 = find_all_flights_in_directory(directory_0804)
    outgoing_flights = merge_flights(
        cheapest_flights_0803, cheapest_flights_0804)

    all_flights = merge_flights(ongoing_flights, outgoing_flights)
    return all_flights

# Main
all_flights = generate_all_flights()
solution = get_random_solution(all_flights)
neighbours = get_neighbours(solution, all_flights)
best_neighbour = find_best_neighbour(solution, neighbours)
print(f'Total price for this neighbour is {calculate_total_price(best_neighbour)}')
print(f'It is cheaper than {calculate_total_price(solution)}')

# print_solution(solution)
# print(f'Total price for this solution is {calculate_total_price(solution)}')
