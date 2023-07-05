#!/usr/bin/python3

from solution_helper import get_random_solution, write_comparison_report
from solution import Solution


def find_minimum_local(solution: Solution) -> Solution:
    current_best = solution
    best_neighbour = current_best.find_best_neighbour()
    while best_neighbour != current_best:
        current_best = best_neighbour
        best_neighbour = current_best.find_best_neighbour()
    return best_neighbour


random_solution = get_random_solution()
minimum = find_minimum_local(random_solution)
write_comparison_report(random_solution, minimum)
