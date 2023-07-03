#!/usr/bin/python3

from typing import List
import random
import math
from extractor_but_better import ALL_FLIGHTS
from solution import Solution
from solution_helper import get_random_solution, write_comparison_report


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
    probability = math.e ** ((- random_neighbour.total_price -
                             solution.total_price)/globals()['temperature'])
    globals()['temperature'] = globals()['temperature']*cool
    if probability >= random.random():
        return random_neighbour
    else:
        return solution


def find_minimum_annealing(solution):
    current_best = solution
    neighbours = current_best.get_neighbour
    best_neighbour = simulated_annealing_neighbour(current_best, neighbours)
    while (globals()['temperature'] >= 20):
        current_best = best_neighbour
        neighbours = current_best.get_neighbour
        best_neighbour = simulated_annealing_neighbour(
            current_best, neighbours)
    return best_neighbour


solution = get_random_solution()
minimum = find_minimum_annealing(solution)
write_comparison_report(solution, minimum)
