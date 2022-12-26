import re
from dataclasses import dataclass

_regex = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore."
    r" Each clay robot costs (\d+) ore."
    r" Each obsidian robot costs (\d+) ore and (\d+) clay."
    r" Each geode robot costs (\d+) ore and (\d+) obsidian."
)


@dataclass
class Blueprint:
    blueprint_id: int
    ore_cost_of_ore_robot: int
    ore_cost_of_clay_robot: int
    ore_cost_of_obsidian_robot: int
    clay_cost_of_obsidian_robot: int
    ore_cost_of_geode_robot: int
    obsidian_cost_of_geode_robot: int

    @classmethod
    def from_string(cls, s):
        (
            blueprint_id,
            ore_cost_of_ore_robot,
            ore_cost_of_clay_robot,
            ore_cost_of_obsidian_robot,
            clay_cost_of_obsidian_robot,
            ore_cost_of_geode_robot,
            obsidian_cost_of_geode_robot,
        ) = _regex.match(s).groups()

        return cls(
            int(blueprint_id),
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


@dataclass
class Player:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    robots: Robots = None
    blueprint: Blueprint = None

    def collect(self):
        self.ore += self.robots.ore_collecting
        self.clay += self.robots.clay_collecting
        self.obsidian += self.robots.obsidian_collecting
        self.geode += self.robots.geode_collecting

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
        self.robots.obsidian_collecting_started += 1


example_1 = (
    "Blueprint 1: Each ore robot costs 4 ore."
    " Each clay robot costs 2 ore."
    " Each obsidian robot costs 3 ore and 14 clay."
    " Each geode robot costs 2 ore and 7 obsidian."
)
example_2 = (
    "Blueprint 2: Each ore robot costs 2 ore."
    " Each clay robot costs 3 ore."
    " Each obsidian robot costs 3 ore and 8 clay."
    " Each geode robot costs 3 ore and 12 obsidian."
)

player = Player(
    robots=Robots(ore_collecting=1),
    blueprint=Blueprint.from_string(example_1),
)

TOTAL_MINUTES = 24

for minute in range(1, 1 + TOTAL_MINUTES):
    print(f"== Minute {minute} ==")
    if player.can_build_geode_robot():
        player.start_build_geode_robot()
    if player.can_build_obsidian_robot():
        player.start_build_obsidian_robot()
    if player.can_build_clay_robot():
        player.start_build_clay_robot()
    if player.can_build_ore_robot():
        player.start_build_ore_robot()
    player.collect()
    player.robots.finish_builds()
    print(player.ore, player.geode)
