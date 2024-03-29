import re
import sys
from functools import cached_property
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
    ore_cost_of_obsid_robot: int
    clay_cost_of_obsid_robot: int
    ore_cost_of_geode_robot: int
    obsid_cost_of_geode_robot: int

    @classmethod
    def from_text(cls, text):
        (
            id_,
            ore_cost_of_ore_robot,
            ore_cost_of_clay_robot,
            ore_cost_of_obsid_robot,
            clay_cost_of_obsid_robot,
            ore_cost_of_geode_robot,
            obsid_cost_of_geode_robot,
        ) = _regex.match(text).groups()

        return cls(
            int(id_),
            int(ore_cost_of_ore_robot),
            int(ore_cost_of_clay_robot),
            int(ore_cost_of_obsid_robot),
            int(clay_cost_of_obsid_robot),
            int(ore_cost_of_geode_robot),
            int(obsid_cost_of_geode_robot),
        )

    @cached_property
    def ore_cost_max(self):
        return max(
            self.ore_cost_of_ore_robot,
            self.ore_cost_of_clay_robot,
            self.ore_cost_of_geode_robot,
            self.ore_cost_of_obsid_robot,
        )


@dataclass
class Robots:
    ore_collecting: int = 0
    clay_collecting: int = 0
    obsid_collecting: int = 0
    geode_collecting: int = 0

    ore_collecting_started: int = 0
    clay_collecting_started: int = 0
    obsid_collecting_started: int = 0
    geode_collecting_started: int = 0

    def copy(self):
        # Custom copies are much faster than copy.copy()
        return Robots(
            ore_collecting=self.ore_collecting,
            clay_collecting=self.clay_collecting,
            obsid_collecting=self.obsid_collecting,
            geode_collecting=self.geode_collecting,
            ore_collecting_started=self.ore_collecting_started,
            clay_collecting_started=self.clay_collecting_started,
            obsid_collecting_started=self.obsid_collecting_started,
            geode_collecting_started=self.geode_collecting_started,
        )


@dataclass
class State:
    time: int = 1
    ore: int = 0
    clay: int = 0
    obsid: int = 0
    geode: int = 0
    blueprint: Blueprint = None
    robots: Robots = None

    def copy(self):
        # Custom copies are much faster than copy.copy()
        return State(
            time=self.time,
            ore=self.ore,
            clay=self.clay,
            obsid=self.obsid,
            geode=self.geode,
            blueprint=self.blueprint,  # no need to copy this
            robots=self.robots.copy(),
        )

    def end_turn(self):
        _robots = self.robots

        # Collection
        self.ore += _robots.ore_collecting
        self.clay += _robots.clay_collecting
        self.obsid += _robots.obsid_collecting
        self.geode += _robots.geode_collecting

        # Moves "started" robots to actual robots
        _robots.ore_collecting += _robots.ore_collecting_started
        _robots.clay_collecting += _robots.clay_collecting_started
        _robots.obsid_collecting += _robots.obsid_collecting_started
        _robots.geode_collecting += _robots.geode_collecting_started

        _robots.ore_collecting_started = 0
        _robots.clay_collecting_started = 0
        _robots.obsid_collecting_started = 0
        _robots.geode_collecting_started = 0

        self.time += 1

    # We only build robot 'X' when:
    # 1) we have the resources
    # 2) we are not already in a position to produce enough 'X'
    #    resources to cover the 'X' cost of any robot (except geodes)
    def can_build_ore_robot(self):
        bp = self.blueprint
        return (
            self.ore >= bp.ore_cost_of_ore_robot
            and self.robots.ore_collecting < bp.ore_cost_max
        )

    def can_build_clay_robot(self):
        bp = self.blueprint
        return (
            self.ore >= bp.ore_cost_of_clay_robot
            and self.robots.clay_collecting < bp.clay_cost_of_obsid_robot
        )

    def can_build_obsid_robot(self):
        bp = self.blueprint
        return (
            self.ore >= bp.ore_cost_of_obsid_robot
            and self.clay >= bp.clay_cost_of_obsid_robot
            and self.robots.obsid_collecting < bp.obsid_cost_of_geode_robot
        )

    def can_build_geode_robot(self):
        return (
            self.ore >= self.blueprint.ore_cost_of_geode_robot
            and self.obsid >= self.blueprint.obsid_cost_of_geode_robot
        )

    def start_build_ore_robot(self):
        self.ore -= self.blueprint.ore_cost_of_ore_robot
        self.robots.ore_collecting_started += 1

    def start_build_clay_robot(self):
        self.ore -= self.blueprint.ore_cost_of_clay_robot
        self.robots.clay_collecting_started += 1

    def start_build_obsid_robot(self):
        self.ore -= self.blueprint.ore_cost_of_obsid_robot
        self.clay -= self.blueprint.clay_cost_of_obsid_robot
        self.robots.obsid_collecting_started += 1

    def start_build_geode_robot(self):
        self.ore -= self.blueprint.ore_cost_of_geode_robot
        self.obsid -= self.blueprint.obsid_cost_of_geode_robot
        self.robots.geode_collecting_started += 1


def upper_bound(state, final_time):
    # This is the theoretical maximum number of  geodes you
    # can have from a state and the final time. It is the sum of:
    # 1) the current geodes
    # 2) the geodes produced from the current robots
    # 3) the geodes produced if you could build a geode robot
    #    each remaining turn.
    remaining_time = final_time - state.time + 1
    return (
        state.geode
        + state.robots.geode_collecting * remaining_time
        + remaining_time * (remaining_time - 1) / 2
    )


def build_state_key(state):
    # That key does not contain the blueprint, as it is supposed to
    # be used in the context of a single blueprint.
    # It also omits the "started" robots, as the key is computed at
    # the beginning of a turn, where no robots has been started yet.
    _robots = state.robots
    return (
        state.ore,
        state.clay,
        state.obsid,
        state.geode,
        _robots.ore_collecting,
        _robots.clay_collecting,
        _robots.obsid_collecting,
        _robots.geode_collecting,
    )


def evaluate_blueprint(text, final_time):
    best_score, best = -1, None

    visited = {}
    stack = [
        State(
            blueprint=Blueprint.from_text(text),
            robots=Robots(ore_collecting=1),
        )
    ]
    while stack:
        state = stack.pop()

        # Check if we already visited that state from another set of actions,
        # and with more time remaining
        key = build_state_key(state)
        if key in visited and visited[key] <= state.time:
            continue
        visited[key] = state.time

        # It is not necessary to inspect actions on last turn,
        # as building things take 1 turn
        if state.time == final_time:
            state.end_turn()
            if best_score < state.geode:
                best_score = state.geode
                best = state
            continue

        next_states = []

        if state.can_build_geode_robot():
            # If we can build a geode robot, other paths
            # are not to be explored
            next_s = state.copy()
            next_s.start_build_geode_robot()
            next_states.append(next_s)
        else:
            # Action of doing nothing and just collecting
            next_s = state.copy()
            next_states.append(next_s)

            if state.can_build_obsid_robot():
                next_s = state.copy()
                next_s.start_build_obsid_robot()
                next_states.append(next_s)

            if state.can_build_clay_robot():
                next_s = state.copy()
                next_s.start_build_clay_robot()
                next_states.append(next_s)

            if state.can_build_ore_robot():
                next_s = state.copy()
                next_s.start_build_ore_robot()
                next_states.append(next_s)

        for next_s in next_states:
            next_s.end_turn()
            if best_score < upper_bound(next_s, final_time):
                stack.append(next_s)

    return best


_input = sys.stdin.read()

# PART 1
#
final_time = 24
result = 0
for row in _input.splitlines():
    best = evaluate_blueprint(row, final_time)
    result += best.blueprint.id_ * best.geode
print(result)


# PART 2
#
final_time = 32
result = 1
for row in _input.splitlines()[:3]:
    best = evaluate_blueprint(row, final_time)
    result *= best.geode
print(result)
