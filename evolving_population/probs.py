import math
import random

from entities import Person

children_count = {0.7: 1, 0.18: 2, 0.08: 3, 0.04: 4, 0.02: 5}


def get_children_count():
    u = random.random()
    for prob in sorted(children_count):
        if u < prob:
            return children_count[prob]
        u -= prob
    return 5


max_children_probs = {0.6: 1, 0.75: 2, 0.35: 3, 0.2: 4, 0.1: 5, 0.05: 100}


def get_max_children():
    u = random.uniform(0, 1)
    for prob in sorted(max_children_probs):
        if u < prob:
            return max_children_probs[prob]
        u -= prob
    return 100


death_probs = {
    (0, 12): (0.25, 0.25),
    (12, 45): (0.1, 0.15),
    (45, 76): (0.3, 0.35),
    (76, 125): (0.7, 0.65),
}


def get_death_age_range(age, gender: str):
    age = age / 12
    for ((lb, ub), (mprob, wprob)) in death_probs.items():
        if lb > age or age > ub:
            continue
        prob = mprob if gender == "male" else wprob
        if random.uniform(0, 1) < prob:
            return ub
    return 125


sex_baby_prob = 0.5


def is_boy():
    return random.uniform(0, 1) <= sex_baby_prob


pregnancy_probs = {
    (0, 12): 0,
    (12, 15): 0.2,
    (15, 21): 0.45,
    (21, 35): 0.8,
    (35, 45): 0.4,
    (45, 60): 0.2,
    (60, 125): 0.05,
}


def gets_pregnant(time: int, person: Person) -> bool:
    age = person.age(time) / 12
    pregnancy_prob = next(
        prob for ((lb, ub), prob) in pregnancy_probs.items() if lb <= age < ub
    )
    return random.uniform(0, 1) < pregnancy_prob


lonely_time_lambda = {
    (0, 12): 0,
    (12, 15): 3,
    (15, 21): 6,
    (21, 35): 6,
    (35, 45): 12,
    (45, 60): 24,
    (60, 125): 48,
}


def get_lonely_time(time: int, person: Person) -> int:
    age = person.age(time) / 12
    try:
        lambda_ = next(
            lambda_ for ((lb, ub), lambda_) in lonely_time_lambda.items() if lb <= age < ub
        )
    except:
        print(age)
        raise
    # return int(-lambda_ * math.log(random.random()))
    return int(-(1 / lambda_) * math.log(random.random()))


breakup_prob = 0.2


def is_breakup():
    return random.uniform(0, 1) <= breakup_prob


looking_for_partner_probs = {
    (0, 12): 0,
    (12, 15): 0.6,
    (15, 21): 0.65,
    (21, 35): 0.8,
    (35, 45): 0.6,
    (45, 60): 0.5,
    (60, 125): 0.2,
}


def is_looking_for_partner(time: int, person: Person) -> bool:
    age = person.age(time) / 12
    try:
        looking_for_partner_prob = next(
            prob
            for ((lb, ub), prob) in looking_for_partner_probs.items()
            if lb <= age < ub
        )
    except:
        print(age, list(looking_for_partner_probs.items()))
        raise
    return random.uniform(0, 1) < looking_for_partner_prob


matching_probs = {
    (0, 5): 0.45,
    (5, 10): 0.4,
    (10, 15): 0.35,
    (15, 20): 0.25,
    (20, 125): 0.15,
}


def is_matching(time: int, person1: Person, person2: Person) -> bool:
    age_gap = abs(person1.age(time) - person2.age(time)) / 12
    matching_prob = next(
        prob for ((lb, ub), prob) in matching_probs.items() if lb <= age_gap < ub
    )
    return random.uniform(0, 1) < matching_prob
