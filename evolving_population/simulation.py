import heapq
import itertools
import sys

from entities import Person
from events import Event, LookingForMatchesEvent, NewFemaleEvent, NewMaleEvent


class Simulation(object):
    def __init__(self, males: int, females: int) -> None:
        self.time = 0
        self.population: list[Person] = []
        self.events: list[Event] = list(
            itertools.chain(
                (NewMaleEvent(0, self.population) for _ in range(males)),
                (NewFemaleEvent(0, self.population) for _ in range(females)),
                (LookingForMatchesEvent(1, self.population),),
            )
        )
        heapq.heapify(self.events)

    def run(self, time: int):
        while len(self.events) > 0:
            event = heapq.heappop(self.events)
            if event.time > 0 and len([p for p in self.population if p.alive]) == 0:
                print("Population finished")
                break

            for new_event in event():
                if new_event.time > time:
                    continue
                heapq.heappush(self.events, new_event)
            self.print_stats(event)

    def print_stats(self, event: Event):
        year = event.time / 12
        population = [p for p in self.population if p.alive]
        print(f"Year: {year} Month: {event.time}")
        print(f"Event: {event.__class__.__name__}")
        print(f"Population Count: {len(population)}")
        print(f"Men Count: {len([p for p in population if p.gender == 'male'])}")
        print(f"Women Count: {len([p for p in population if p.gender == 'female'])}")
        print()


if __name__ == "__main__":
    sim = Simulation(int(sys.argv[1]), int(sys.argv[2]))
    sim.run(1200)
