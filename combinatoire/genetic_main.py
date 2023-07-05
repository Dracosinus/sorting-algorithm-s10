#!/usr/bin/python3

from typing import List
import random
import math

from solution import Solution
from circular_linked_list import CircularLinkedList
from solution_helper import get_random_solution


def find_best_solution_of_pool(solution_pool: List[Solution]) -> Solution:
    """Returns the best Solution of a given solution list cost-wise

    Args:
        solution_pool (List[Solution])

    Returns:
        Solution: 
    """
    current_best = solution_pool[0]
    for solution in solution_pool:
        if solution.total_price < current_best.total_price:
            current_best = solution
    return current_best


def cross_parents(first_parent, second_parent, gene_slicer):
    """cross two parents around a gene slicer to generate two childrens

    Args:
        first_parent (Solution):
        second_parent (Solution):
        gene_slicer (int): where to cut the parents genes

    Returns:
        (Solution, Solution): the two childrens
    """
    first_child = second_child = {}
    slice_count = 0
    first_parent_map = first_parent.solution_map
    second_parent_map = second_parent.solution_map
    for key in first_parent_map.keys():
        if slice_count < gene_slicer:
            first_child[key] = first_parent_map[key]
            second_child[key] = second_parent_map[key]
        else:
            first_child[key] = second_parent_map[key]
            second_child[key] = first_parent_map[key]
        slice_count = slice_count+1
    return (Solution(first_child), Solution(second_child))


def elitism(solution_pool, survivors_percent):
    """only a percentage of the best element from a solution survives

    Args:
        solution_pool (List[Solution])
        survivors_percent (float): percentage of survivors

    Returns:
        List[Solution]
    """
    survivors_amount = math.floor(len(solution_pool)*survivors_percent)
    survivors = []
    while len(survivors) != survivors_amount:
        best_solution = find_best_solution_of_pool(solution_pool)
        survivors.append(best_solution)
        solution_pool.remove(best_solution)
    return survivors


def genetic_main(genetic_pool_members=100, survivors_percent=0.1, crossing_expected_percent=0.4, pool_injection_percent=0.1, max_generation=5):
    """genetic logic get an heuristic set of decent solutions
    At every generation, many pool members 'dies' letting a small amount of performant survivors
    We cross the ~~genes~~ flights of the survivors to generate new solutions
    We keep the survivors
    We also use new blood to allow expanding solutions
    We also use neighbours from the survivors

    Args:
        genetic_pool_members (int, optional): Amount of solutions at each generation. Defaults to 100.
        survivors_percent (float, optional): Surviving solutions at each generation. Defaults to 0.1.
        crossing_expected_percent (float, optional): Percentage of solutions built by crossing survivors to replace dead. Defaults to 0.4.
        pool_injection_percent (float, optional): New solutions added to the pool. Defaults to 0.1.
        max_generation (int, optional): The amount of generations. Defaults to 5.
    """
    genetic_solution_pool = []

    for i in range(genetic_pool_members):
        genetic_solution_pool.append(get_random_solution())

    generation_pool = genetic_solution_pool
    for i in range(max_generation):
        survivors = elitism(generation_pool, survivors_percent)
        next_generation_pool = cross_survivors(survivors, math.floor(
            genetic_pool_members*crossing_expected_percent))
        for survivor in survivors:
            if len(next_generation_pool) < genetic_pool_members:
                next_generation_pool.append(survivor)

        for i in range(math.floor(pool_injection_percent*genetic_pool_members)):
            if len(next_generation_pool) < genetic_pool_members:
                next_generation_pool.append(get_random_solution())

        next_generation_pool = list(set(next_generation_pool))
        while len(next_generation_pool) < genetic_pool_members:
            close_neighbour = random.choice(
                random.choice(survivors).get_neighbours())
            if close_neighbour not in next_generation_pool:
                next_generation_pool.append(close_neighbour)

        generation_pool = next_generation_pool

    final_survivors = elitism(generation_pool, survivors_percent)
    print(f'After {max_generation} generations')
    for solution in final_survivors:
        solution.write_report()
    print("\nbest solution of pool is :")
    best_solution = find_best_solution_of_pool(final_survivors)
    best_solution.write_report()


def cross_survivors(survivors, crossing_expected):
    """Cross survivors between themselves by slicing them together randomly

    Args:
        survivors (List[solution]): solution pool that you want to evolve from
        crossing_expected (int, optional): the amount of childs. Defaults to 40.

    Returns:
        List[solution]: wider solution pool to work with
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
        (first_child, second_child) = cross_parents(
            first_parent, second_parent, gene_slicer)
        crossed_generation_pool.append(first_child)
        crossed_generation_pool.append(second_child)
        survivor_node = survivor_node.next

    while len(crossed_generation_pool) > crossing_expected:
        crossed_generation_pool.pop()

    return crossed_generation_pool


# Main
genetic_main(max_generation=150)
