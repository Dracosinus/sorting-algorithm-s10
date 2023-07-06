#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import os
from datetime import datetime
from flight import Flight

LAST_BUS_DEPART = datetime.fromisoformat('2010-07-27 17:00:00')
FIRST_BUS_ARRIVAL = datetime.fromisoformat('2010-08-03 15:00:00')


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
            flight.conf_role = 'incoming'
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

    for key, flights in flights1.items():
        merged_flights[key] = flights

    for key, flights in flights2.items():
        if key in merged_flights:
            merged_flights[key].extend(flights)
        else:
            merged_flights[key] = flights

    return merged_flights


def generate_all_flights():
    base_directory = os.getcwd()+'/'

    directory_0726 = 'ThirdParty/FlightData/2010/07-26/'
    cheapest_flights_0726 = find_all_flights_in_directory(
        base_directory+directory_0726)

    directory_0727 = 'ThirdParty/FlightData/2010/07-27/'
    cheapest_flights_0727 = find_all_flights_in_directory(
        base_directory+directory_0727)
    ongoing_flights = merge_flights(
        cheapest_flights_0726, cheapest_flights_0727)

    directory_0803 = 'ThirdParty/FlightData/2010/08-03/'
    cheapest_flights_0803 = find_all_flights_in_directory(
        base_directory+directory_0803)

    directory_0804 = 'ThirdParty/FlightData/2010/08-04/'
    cheapest_flights_0804 = find_all_flights_in_directory(
        base_directory+directory_0804)
    outgoing_flights = merge_flights(
        cheapest_flights_0803, cheapest_flights_0804)

    all_flights = merge_flights(ongoing_flights, outgoing_flights)
    return all_flights


ALL_FLIGHTS = generate_all_flights()
