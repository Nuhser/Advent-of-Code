from collections import defaultdict
from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        almanac = aoc.parse_input_with_blocks(puzzle_input, " ")

        self.seeds = [int(seed) for seed in almanac[0][0][1:]]

        self.maps: dict[tuple[str, str], list[dict[str, int]]] = {}
        for map in almanac[1:]:
            map_key: tuple[str, str] = map[0][0].split("-")[0], map[0][0].split("-")[2]

            self.maps[map_key] = list()
            for entry in map[1:]:
                self.maps[map_key].append({"from": int(entry[1]), "to": int(entry[0]), "range": int(entry[2])-1})

        if (self.verbose):
            print(f"Seeds: {", ".join(str(seed) for seed in self.seeds)}")
            print(f"Maps: {self.maps}\n")


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        locations: list[int] = []
        for seed in self.seeds:
            if (self.verbose):
                print(f"Starting with seed {seed}")

            for key, map in self.maps.items():
                if (self.verbose):
                    print(f"Mapping from {key[0]} to {key[1]}...")

                for mapping in map:
                    diff = seed - mapping["from"]
                    if (diff >= 0 and diff <= mapping["range"]):
                        seed = mapping["to"] + diff

                        if (self.verbose):
                            print(f"Found matching mapping: {mapping}")

                        break

            locations.append(seed)

        closest_location = min(locations)

        return f"Final locations: {", ".join(str(location) for location in locations)}\nClosest Location: {closest_location}", closest_location


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution isn't implemented yet!")