import random
from solution import Solution
from time_helper import divide_mins_to_days_hours_mins
from extractor_but_better import ALL_FLIGHTS


def write_comparison_report(solution: Solution, minimum: Solution):
    minimum.write_report()
    print(f'It is cheaper than {solution.total_price} where')
    (jours, heures, minutes) = divide_mins_to_days_hours_mins(
        solution.calculate_spent_time_in_mins())
    print(
        f"Attendees would have waited : {jours} day(s), {heures} hour(s), {minutes} minute(s)")


def get_random_solution():
    solution = {}
    for key, flights_list in ALL_FLIGHTS.items():
        solution[key] = random.choice(flights_list)
    return Solution(solution)
