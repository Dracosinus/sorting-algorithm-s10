import random
from solution import Solution
from flight_extractor import ALL_FLIGHTS


def write_comparison_report(solution: Solution, minimum: Solution):
    minimum.write_report()
    print('\n It is, in theory, cheaper than the solution it derives from :')
    solution.write_report()

def get_random_solution():
    solution = {}
    for key, flights_list in ALL_FLIGHTS.items():
        solution[key] = random.choice(flights_list)
    return Solution(solution)
