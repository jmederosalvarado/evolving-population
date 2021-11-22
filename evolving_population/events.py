import itertools
import random
from abc import abstractmethod
from typing import Iterable

import probs
from entities import Female, Male, Person


class Event(object):
    def __init__(self, time: int, population: list[Person]) -> None:
        self.time = time
        self.population = population

    @abstractmethod
    def __call__(self) -> Iterable["Event"]:
        pass

    def __lt__(self, __o: object) -> int:
        return isinstance(__o, Event) and self.time.__lt__(__o.time)


class NewPersonEvent(Event):
    def __init__(self, time: int, population: list[Person], age: int = None) -> None:
        super().__init__(time, population)
        self.age = age

    def __call__(self) -> Iterable["Event"]:
        return super().__call__()

    def get_death_event(self, person: Person):
        ub = probs.get_death_age_range(person.age(self.time), person.gender)
        lb = person.age(self.time) // 12
        death_age = int(random.uniform(lb, ub) * 12 + random.uniform(0, 12))
        print("death to", death_age, lb, self.time + (death_age - lb))
        return DeathEvent(self.time + (death_age - lb * 12), self.population, person)


class NewMaleEvent(NewPersonEvent):
    def __init__(self, time: int, population: list[Person], age: int = None) -> None:
        super().__init__(time, population, age)

    def __call__(self) -> Iterable["Event"]:
        age = int(random.uniform(0, 100)) * 12 if self.age is None else self.age
        person = Male(
            self.time - age,
            probs.get_max_children(),
        )
        self.population.append(person)
        print("----------- created person", age / 12)
        yield self.get_death_event(person)


class NewFemaleEvent(NewPersonEvent):
    def __init__(self, time: int, population: list[Person], age: int = None) -> None:
        super().__init__(time, population, age)

    def __call__(self) -> Iterable["Event"]:
        age = int(random.uniform(0, 100)) * 12 if self.age is None else self.age
        person = Female(
            self.time - age,
            probs.get_max_children(),
        )
        self.population.append(person)
        yield self.get_death_event(person)


class DeathEvent(Event):
    def __init__(
        self,
        time: int,
        population: list[Person],
        person: Person,
    ) -> None:
        super().__init__(time, population)
        self.person = person

    def __call__(self) -> Iterable["Event"]:
        self.person.die()
        if self.person.partner is not None and self.person.partner.alive:
            yield WidowEvent(self.time, self.population, self.person.partner)


class LookingForMatchesEvent(Event):
    def __init__(self, time: int, population: list[Person]) -> None:
        super().__init__(time, population)

    def __call__(self) -> Iterable["Event"]:
        candidates = [
            person
            for person in self.population
            if person.alive
            and person.partner is None
            and not person.crying
            and probs.is_looking_for_partner(self.time, person)
        ]

        matched = set()
        for p1, p2 in itertools.combinations(candidates, 2):
            if p1 in matched or p2 in matched or p1.gender == p2.gender:
                continue
            if not probs.is_matching(self.time, p1, p2):
                continue
            matched = matched.union((p1, p2))
            yield MatchingEvent(self.time, self.population, p1, p2)

        yield LookingForMatchesEvent(self.time + 1, self.population)
        if len(matched) > 0:
            print("-------------------- matched", len(matched))


class MatchingEvent(Event):
    def __init__(
        self,
        time: int,
        population: list[Person],
        person1: Person,
        person2: Person,
    ) -> None:
        super().__init__(time, population)
        self.person1 = person1
        self.person2 = person2

    def __call__(self) -> Iterable["Event"]:
        self.person1.match(self.person2)
        self.person2.match(self.person1)
        if probs.is_breakup():
            yield BreakUpEvent(
                int(
                    # 50 here is arbitrary
                    random.uniform(self.time + 1, self.time + 50 * 12)
                ),
                self.population,
                self.person1,
                self.person2,
            )
        man = next(p for p in (self.person1, self.person2) if isinstance(p, Male))
        woman = next(p for p in (self.person1, self.person2) if isinstance(p, Female))
        yield TryGetPregnantEvent(self.time, self.population, man, woman)


class TryGetPregnantEvent(Event):
    def __init__(
        self, time: int, population: list[Person], man: Person, woman: Female
    ) -> None:
        super().__init__(time, population)
        self.woman = woman
        self.man = man

    def __call__(self) -> Iterable["Event"]:
        if self.woman.partner != self.man:
            return []

        if (
            not self.woman.pregnant
            and self.man.children_left > 0
            and self.woman.children_left > 0
            and probs.gets_pregnant(self.time, self.woman)
        ):
            self.woman.get_pregnant()
            yield GiveBirthEvent(self.time + 9, self.population, self.man, self.woman)
        else:
            # wait 3 months to try get pregnant again
            yield TryGetPregnantEvent(
                self.time + 3, self.population, self.man, self.woman
            )


class BreakUpEvent(Event):
    def __init__(
        self, time: int, population: list[Person], person1: Person, person2: Person
    ) -> None:
        super().__init__(time, population)
        self.person1 = person1
        self.person2 = person2

    def __call__(self) -> Iterable["Event"]:
        if not self.person1.alive or not self.person2.alive:
            return []
        for person in (self.person1, self.person2):
            person.get_lonely()
            yield LonelyTimeOverEvent(
                self.time + probs.get_lonely_time(self.time, person),
                self.population,
                person,
            )


class WidowEvent(Event):
    def __init__(self, time: int, population: list[Person], person: Person) -> None:
        super().__init__(time, population)
        self.person = person

    def __call__(self) -> Iterable["Event"]:
        self.person.get_lonely()
        yield LonelyTimeOverEvent(
            self.time + probs.get_lonely_time(self.time, self.person),
            self.population,
            self.person,
        )


class LonelyTimeOverEvent(Event):
    def __init__(self, time: int, population: list[Person], person: Person) -> None:
        super().__init__(time, population)
        self.person = person

    def __call__(self) -> Iterable["Event"]:
        self.person.move_on()
        return []


class GiveBirthEvent(Event):
    def __init__(
        self, time: int, population: list[Person], man: Person, woman: Person
    ) -> None:
        super().__init__(time, population)
        self.man = man
        self.woman = woman

    def __call__(self) -> Iterable["Event"]:
        if not self.woman.alive:
            return []
        if self.man.alive:
            self.man.have_children(probs.get_children_count())
        self.woman.have_children(probs.get_children_count())
        if probs.is_boy():
            yield NewMaleEvent(self.time, self.population, 0)
        else:
            yield NewFemaleEvent(self.time, self.population, 0)
