import re
import sys
from dataclasses import dataclass

_regex = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore."
    r" Each clay robot costs (\d+) ore."
    r" Each obsidian robot costs (\d+) ore and (\d+) clay."
    r" Each geode robot costs (\d+) ore and (\d+) obsidian."
)


@dataclass
class Blueprint:
    id_: int
    ore_cost_of_ore_robot: int
    ore_cost_of_clay_robot: int
    ore_cost_of_obsidian_robot: int
    clay_cost_of_obsidian_robot: int
    ore_cost_of_geode_robot: int
    obsidian_cost_of_geode_robot: int

    @classmethod
    def from_text(cls, text):
        (
            id_,
            ore_cost_of_ore_robot,
            ore_cost_of_clay_robot,
            ore_cost_of_obsidian_robot,
            clay_cost_of_obsidian_robot,
            ore_cost_of_geode_robot,
            obsidian_cost_of_geode_robot,
        ) = _regex.match(text).groups()

        return cls(
            int(id_),
            int(ore_cost_of_ore_robot),
            int(ore_cost_of_clay_robot),
            int(ore_cost_of_obsidian_robot),
            int(clay_cost_of_obsidian_robot),
            int(ore_cost_of_geode_robot),
            int(obsidian_cost_of_geode_robot),
        )


@dataclass
class Robots:
    ore_collecting: int = 0
    clay_collecting: int = 0
    obsidian_collecting: int = 0
    geode_collecting: int = 0

    ore_collecting_started: int = 0
    clay_collecting_started: int = 0
    obsidian_collecting_started: int = 0
    geode_collecting_started: int = 0

    def finish_builds(self):
        self.ore_collecting += self.ore_collecting_started
        self.clay_collecting += self.clay_collecting_started
        self.obsidian_collecting += self.obsidian_collecting_started
        self.geode_collecting += self.geode_collecting_started

        self.ore_collecting_started = 0
        self.clay_collecting_started = 0
        self.obsidian_collecting_started = 0
        self.geode_collecting_started = 0

    def copy(self):
        return Robots(
            ore_collecting=self.ore_collecting,
            clay_collecting=self.clay_collecting,
            obsidian_collecting=self.obsidian_collecting,
            geode_collecting=self.geode_collecting,
            ore_collecting_started=self.ore_collecting_started,
            clay_collecting_started=self.clay_collecting_started,
            obsidian_collecting_started=self.obsidian_collecting_started,
            geode_collecting_started=self.geode_collecting_started,
        )


@dataclass
class State:
    time: int = 1
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    blueprint: Blueprint = None
    robots: Robots = None

    def copy(self):
        return State(
            time=self.time,
            ore=self.ore,
            clay=self.clay,
            obsidian=self.obsidian,
            geode=self.geode,
            blueprint=self.blueprint,
            robots=self.robots.copy(),
        )

    def end_turn(self):
        robots = self.robots

        # Collection
        self.ore += robots.ore_collecting
        self.clay += robots.clay_collecting
        self.obsidian += robots.obsidian_collecting
        self.geode += robots.geode_collecting

        robots.finish_builds()
        self.time += 1

    def can_build_ore_robot(self):
        return self.ore >= self.blueprint.ore_cost_of_ore_robot

    def can_build_clay_robot(self):
        return self.ore >= self.blueprint.ore_cost_of_clay_robot

    def can_build_obsidian_robot(self):
        return (
            self.ore >= self.blueprint.ore_cost_of_obsidian_robot
            and self.clay >= self.blueprint.clay_cost_of_obsidian_robot
        )

    def can_build_geode_robot(self):
        return (
            self.ore >= self.blueprint.ore_cost_of_geode_robot
            and self.obsidian >= self.blueprint.obsidian_cost_of_geode_robot
        )

    def start_build_ore_robot(self):
        self.ore -= self.blueprint.ore_cost_of_ore_robot
        self.robots.ore_collecting_started += 1

    def start_build_clay_robot(self):
        self.ore -= self.blueprint.ore_cost_of_clay_robot
        self.robots.clay_collecting_started += 1

    def start_build_obsidian_robot(self):
        self.ore -= self.blueprint.ore_cost_of_obsidian_robot
        self.clay -= self.blueprint.clay_cost_of_obsidian_robot
        self.robots.obsidian_collecting_started += 1

    def start_build_geode_robot(self):
        self.ore -= self.blueprint.ore_cost_of_geode_robot
        self.obsidian -= self.blueprint.obsidian_cost_of_geode_robot
        self.robots.geode_collecting_started += 1


LAST_MINUTE = 24


def upper_bound(state):
    remaining_time = LAST_MINUTE - state.time + 1
    return (
        state.geode
        + state.robots.geode_collecting * remaining_time
        + remaining_time * (remaining_time + 1) // 2
    )


def evaluate_blueprint(text):
    best_score, best = -1, None

    stack = [
        State(
            blueprint=Blueprint.from_text(text),
            robots=Robots(ore_collecting=1),
        )
    ]
    while stack:
        state = stack.pop()

        # It is not necessary to inspect actions on last turn,
        # as building things take 1 turn
        if state.time == LAST_MINUTE:
            state.end_turn()
            if best_score < state.geode:
                best_score = state.geode
                best = state
            continue

        new_s = state.copy()
        new_s.end_turn()
        if upper_bound(new_s) > best_score:
            stack.append(new_s)

        if state.can_build_geode_robot():
            new_s = state.copy()
            new_s.start_build_geode_robot()
            new_s.end_turn()
            if upper_bound(new_s) > best_score:
                stack.append(new_s)

        if state.can_build_obsidian_robot():
            new_s = state.copy()
            new_s.start_build_obsidian_robot()
            new_s.end_turn()
            if upper_bound(new_s) > best_score:
                stack.append(new_s)

        if state.can_build_clay_robot():
            new_s = state.copy()
            new_s.start_build_clay_robot()
            new_s.end_turn()
            if upper_bound(new_s) > best_score:
                stack.append(new_s)

        if state.can_build_ore_robot():
            new_s = state.copy()
            new_s.start_build_ore_robot()
            new_s.end_turn()
            if upper_bound(new_s) > best_score:
                stack.append(new_s)

    quality_level = best.geode * best.blueprint.id_
    # print(best.blueprint.id_, ":", best.geode, quality_level)
    return quality_level


print(sum(evaluate_blueprint(row.rstrip()) for row in sys.stdin))
