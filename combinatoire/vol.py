#!/usr/bin/python3

from typing import List
import random
import math
from circular_linked_list import CircularLinkedList
import all_flights_extractor
from solution.py import Solution


ALL_FLIGHTS = all_flights_extractor.generate_all_flights()


def get_random_solution():
    solution = {}
    for key, flights_list in ALL_FLIGHTS.items():
        solution[key] = random.choice(flights_list)
    return Solution(solution)


def divide_mins_to_days_hours_mins(duree_minutes):
    jours = duree_minutes // (24 * 60)
    heures = (duree_minutes // 60) % 24
    minutes = duree_minutes % 60
    return (jours, heures, minutes)


def find_best_neighbour(solution, neighbours):
    best_neighbour = solution
    best_price = best_neighbour.total_price
    for neighbour in neighbours:
        if neighbour.total_price < best_price:
            best_neighbour = neighbour
            best_price = neighbour.total_price
    return best_neighbour


def find_minimum_local(solution: List[Solution]):
    current_best = solution
    best_neighbour = find_best_neighbour(current_best, current_best.neighbours)
    while best_neighbour != current_best:
        current_best = best_neighbour
        best_neighbour = find_best_neighbour(
            current_best, current_best.neighbours)
    return best_neighbour


def find_best_solution_of_pool(solution_pool: List[Solution]):
    current_best = solution_pool[0]
    for solution in solution_pool:
        if solution.total_price < current_best.total_price:
            current_best = solution
    return current_best


def simulated_annealing_neighbour(solution, neighbours):
    cool = 0.95
    if 'temperature' not in globals():
        globals()['temperature'] = 10000
    random_neighbour = random.choice(neighbours)
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
        genetic_solution_pool.append(get_random_solution())

    generation_pool = genetic_solution_pool
    for i in range(max_generation):
        survivors = elitism(generation_pool, survivors_percent)
        next_generation_pool = cross_survivors(survivors)

        for i in range(math.floor(pool_injection_percent*genetic_pool_members)):
            if len(next_generation_pool) < genetic_pool_members:
                next_generation_pool.append(get_random_solution())

        while len(next_generation_pool) < genetic_pool_members:
            next_generation_pool.append(random.choice(
                get_neighbours(random.choice(survivors))))

        generation_pool = next_generation_pool

    final_survivors = elitism(generation_pool, survivors_percent)
    print(f'After {max_generation} generations')
    for solution in final_survivors:
        write_solution_report(solution)
    print("\nbest solution of pool is :")
    best_solution = find_best_solution_of_pool(final_survivors)
    write_solution_report(best_solution)


def cross_survivors(survivors, crossing_expected=40):
    """Cross survivors between themselves by slicing them together randomly

    Args:
        survivors (List<solution>): solution pool that you want to evolve from
        crossing_expected (int, optional): the amount of chil. Defaults to 40.

    Returns:
        List<solution>: wider solution pool to work with
    """
    crossed_generation_pool = []
    survivors_amount = len(survivors)
    survivor_id_list = CircularLinkedList()
    for i in range(survivors_amount):
        survivor_id_list.append(i)
    survivor_node = survivor_id_list.head

    while len(crossed_generation_pool) < crossing_expected:

        random_second_parent_id = random.randint(0, survivors_amount-1)
        while random_second_parent_id == survivor_node.data:
            random_second_parent_id = random.randint(0, survivors_amount-1)

        gene_slicer = random.randint(0, 17)
        first_parent = survivors[survivor_node.data]
        second_parent = survivors[random_second_parent_id]
        (first_child, second_child) = slice(
            first_parent, second_parent, gene_slicer)
        crossed_generation_pool.append(find_minimum_local(first_child))
        crossed_generation_pool.append(find_minimum_local(second_child))
        survivor_node = survivor_node.next

    while len(crossed_generation_pool) > crossing_expected:
        crossed_generation_pool.pop()

    return crossed_generation_pool


# Main
genetic_main()
