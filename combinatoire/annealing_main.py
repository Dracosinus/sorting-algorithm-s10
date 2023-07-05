#!/usr/bin/python3

from typing import List
import random
import math
from solution import Solution
from solution_helper import get_random_solution, write_comparison_report


def simulated_annealing_neighbour(solution: Solution, neighbours: List[Solution]) -> Solution:
    cool = 0.95
    if 'temperature' not in globals():
        globals()['temperature'] = 10000
    random_neighbour = random.choice(neighbours)
    probability = math.e ** ((- random_neighbour.total_price -
                             solution.total_price)/globals()['temperature'])
    globals()['temperature'] = globals()['temperature']*cool

    random_float = random.random()
    # print(f'probablility is {probability} compared to {random_float}')
    # TOFIX : probability is ALWAYS too small, order e-10, it gets worse. Cannot return anything but solution

    if probability >= random_float:
        return random_neighbour
    else:
        return solution


def find_minimum_annealing(solution: Solution) -> Solution:
    """executes annealing until the temperature is low enough

    Args:
        solution (Solution): 

    Returns:
        Solution: annealed Solution
    """
    solution = simulated_annealing_neighbour(
        solution, solution.get_neighbours())
    while (globals()['temperature'] >= 20):
        solution = simulated_annealing_neighbour(
            solution, solution.get_neighbours())
    return solution


random_solution = get_random_solution()
minimum = find_minimum_annealing(random_solution)
write_comparison_report(random_solution, minimum)
