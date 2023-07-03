#!/usr/bin/python3

import xml.etree.ElementTree as ET
import os
import random
import copy
import math
from datetime import datetime, time

LAST_BUS_DEPART = datetime.fromisoformat('2010-07-27 17:00:00')
FIRST_BUS_ARRIVAL = datetime.fromisoformat('2010-08-03 15:00:00')
PRICE_PER_MINUTE = 5


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


ALL_FLIGHTS = generate_all_flights()


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


def get_random_solution():
    solution = {}
    for key, flights_list in ALL_FLIGHTS.items():
        solution[key] = random.choice(flights_list)
    return solution


def print_solution(solution):
    for key, flight in solution.items():
        print(f'For Key : {key}')
        print_flight(flight)


def calculate_total_price(solution):
    total_price = 0
    for flight in solution.values():
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


def calculate_spent_time_in_mins(solution):
    spent_time = 0
    for flight in solution.values():
        if flight.conf_role == 'incoming':
            duration = LAST_BUS_DEPART - flight.arrive
        else:
            duration = flight.depart - FIRST_BUS_ARRIVAL
        difference_in_mins = duration.total_seconds() / 60.0
        spent_time += difference_in_mins
        # (days, hours, mins) = divide_mins_to_days_hours_mins(difference_in_mins)
        # print(f'we just added {days} days, {hours} hours, {mins} mins')
    return spent_time


def divide_mins_to_days_hours_mins(duree_minutes):
    jours = duree_minutes // (24 * 60)
    heures = (duree_minutes // 60) % 24
    minutes = duree_minutes % 60
    return (jours, heures, minutes)


def get_neighbours(solution):
    neighbours = []
    for key, flight in solution.items():
        flight_list = ALL_FLIGHTS[key]
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
    best_neighbour = solution
    best_price = calculate_total_price(best_neighbour)
    for neighbour in neighbours:
        if calculate_total_price(neighbour) < best_price:
            best_neighbour = neighbour
            best_price = calculate_total_price(neighbour)
    return best_neighbour


def find_minimum_local(solution):
    current_best = solution
    neighbours = get_neighbours(current_best)
    best_neighbour = find_best_neighbour(current_best, neighbours)
    while (best_neighbour != current_best):
        current_best = best_neighbour
        neighbours = get_neighbours(current_best)
        best_neighbour = find_best_neighbour(current_best, neighbours)
    return best_neighbour


def find_best_solution_of_pool(solution_pool):
    current_best = solution_pool[0]
    for solution in solution_pool:
        if calculate_total_price(solution) < calculate_total_price(current_best):
            current_best = solution
    return current_best


def simulated_annealing_neighbour(solution, neighbours):
    cool = 0.95
    if 'temperature' not in globals():
        globals()['temperature'] = 10000
    random_neighbour = random.choice(neighbours)
    # probability = math.e ** -(abs(calculate_total_price(random_neighbour) - calculate_total_price(solution))/globals()['temperature'])
    probability = math.e ** ((- calculate_total_price(random_neighbour) -
                             calculate_total_price(solution))/globals()['temperature'])
    globals()['temperature'] = globals()['temperature']*cool
    if probability >= random.random():
        return random_neighbour
    else:
        return solution


def find_minimum_annealing(solution):
    current_best = solution
    neighbours = get_neighbours(current_best)
    best_neighbour = simulated_annealing_neighbour(current_best, neighbours)
    while (globals()['temperature'] >= 20):
        current_best = best_neighbour
        neighbours = get_neighbours(current_best)
        best_neighbour = simulated_annealing_neighbour(
            current_best, neighbours)
    return best_neighbour


def write_solution_report(solution):
    print(
        f'Total price for this solution is {calculate_total_price(solution)}')
    duree_minutes = calculate_spent_time_in_mins(solution)
    (jours, heures, minutes) = divide_mins_to_days_hours_mins(duree_minutes)
    print(
        f"Attendees will wait {duree_minutes} mins, meaning : {jours} day(s), {heures} hour(s), {minutes} minute(s)")


def write_comparison_report(solution, minimum):
    write_solution_report(minimum)
    print(f'It is cheaper than {calculate_total_price(solution)} where')
    duree_minutes = calculate_spent_time_in_mins(solution)
    (jours, heures, minutes) = divide_mins_to_days_hours_mins(duree_minutes)
    print(
        f"Attendees would have waited : {jours} day(s), {heures} hour(s), {minutes} minute(s)")


def monte_carlo_main(solution):
    minimum = find_minimum_local(solution)
    write_comparison_report(solution, minimum)


def annealing_main(solution):
    minimum = find_minimum_annealing(solution)
    write_comparison_report(solution, minimum)


def slice(first_parent, second_parent, gene_slicer):
    """cross two parents around a gene slicer to generate two childrens

    Args:
        first_parent (solution): 
        second_parent (solution): 
        gene_slicer (int): where to cut the parents genes

    Returns:
        (solution, solution): the two childrens
    """
    first_child = second_child = {}
    slice_count = 0
    for key in first_parent.keys():
        if slice_count < gene_slicer:
            first_child[key] = first_parent[key]
            second_child[key] = second_parent[key]
        else:
            first_child[key] = second_parent[key]
            second_child[key] = first_parent[key]
        slice_count = slice_count+1
    return (first_child, second_child)

def elitism(solution_pool, survivors_percent):
    """only a percentage of the best element from a solution survives

    Args:
        solution_pool (List<solution>)
        survivors_percent (float): percentage of survivors

    Returns:
        List<solution>
    """
    survivors_amount = math.floor(len(solution_pool)*survivors_percent)
    survivors = []
    while len(survivors) != survivors_amount:
        best_solution = find_best_solution_of_pool(solution_pool)
        survivors.append(best_solution)
        solution_pool.remove(best_solution)
    return survivors
 

def genetic_main(genetic_pool_members=100, survivors_percent=0.1, pool_injection_percent=0.1, max_generation=5):
    genetic_solution_pool = []
    
    for i in range(genetic_pool_members):
        solution = get_random_solution()
        genetic_solution_pool.append(solution)

    generation_pool = genetic_solution_pool
    for i in range(max_generation):
        survivors = elitism(generation_pool, survivors_percent)
        next_generation_pool = mutate_solution(survivors)

        for i in range(math.floor(pool_injection_percent*genetic_pool_members)):
            if len(next_generation_pool) < genetic_pool_members:
                next_generation_pool.append(get_random_solution())

        while len(next_generation_pool) != genetic_pool_members:
            next_generation_pool.append(random.choice(get_neighbours(random.choice(survivors))))

        generation_pool = next_generation_pool

    final_survivors = elitism(generation_pool, survivors_percent)
    print(f'After {max_generation} generations')
    for solution in final_survivors:
        write_solution_report(solution)
    print("best solution of pool is :")
    best_solution = find_best_solution_of_pool(final_survivors)
    write_solution_report(best_solution)


def mutate_solution(genetic_solution_pool):
    generation_pool = []
    for k in range(int(len(generation_pool)/2)):
        gene_slicer = random.randint(0, 17)
        first_parent = genetic_solution_pool[2*k]
        second_parent = genetic_solution_pool[2*k+1]
        (first_child, second_child) = slice(
            first_parent, second_parent, gene_slicer)
        generation_pool.append(find_minimum_local(first_child))
        generation_pool.append(find_minimum_local(second_child))
    return generation_pool


# Main
genetic_main()
