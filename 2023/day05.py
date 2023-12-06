from random import seed
from tracemalloc import start
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
            print(f"Maps:\n{"\n".join(str(value) for value in self.maps.values())}\n")


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
        seed_ranges: list[dict[str, int]] = []
        for idx in range(0, len(self.seeds), 2):
            seed_ranges.append({"from": self.seeds[idx], "range": self.seeds[idx+1]-1})
            
        if (self.verbose):
            print(f"Original Seed Ranges: {seed_ranges}\n")
        
        for key, map in self.maps.items():
            seed_ranges = self.map_seed_ranges_recursively(map, seed_ranges)

            if (self.verbose):
                print(f"Seed Ranges after mapping {key[0]} -> {key[1]}: {seed_ranges}\n")

        if (self.verbose):
            print(f"Final Seed Ranges: {seed_ranges}")

        closest_location = min(seed_range["from"] for seed_range in seed_ranges)

        return f"Closest Location: {closest_location}", closest_location


    def map_seed_ranges_recursively(self, map: list[dict[str, int]], seed_ranges: list[dict[str, int]]) -> list[dict[str, int]]:
        """
        Possible cases:

            1. complete seed range left of mapping range --> skip
            2. complete seed range right of mapping range --> skip
            3. complete seed range inside mapping range (or the same as mapping range)
            4. seed range starts left of and ends inside mapping range
            5. seed range starts inside and ends right of mapping range
            6. seed range starts left of and ends right of mapping range
        """

        mapped_seed_ranges: list[dict[str, int]] = []
        new_seed_ranges: list[dict[str, int]] = []

        for seed_range in seed_ranges:
            mapping_found = False
            for mapping in map:
                start_diff = seed_range["from"] - mapping["from"]
                
                if (start_diff < 0): # seed start left of mapping start
                    start_diff = abs(start_diff)

                    # case 1
                    if (start_diff > seed_range["range"]):
                        continue

                    # case 4
                    elif (seed_range["range"] - start_diff <= mapping["range"]):
                        new_seed_ranges.append({"from": seed_range["from"], "range": start_diff - 1}) # left of mapping
                        mapped_seed_ranges.append({"from": mapping["to"], "range": seed_range["range"] - start_diff + 1}) # inside mapping

                        mapping_found = True
                        break

                    # case 6
                    else:
                        new_seed_ranges.append({"from": seed_range["from"], "range": start_diff - 1}) # left of mapping
                        mapped_seed_ranges.append({"from": mapping["to"], "range": mapping["range"]}) # inside mapping
                        new_seed_ranges.append({"from": mapping["from"] + mapping["range"] + 1, "range": seed_range["range"] - (mapping["range"] + start_diff + 1)}) # right of mapping

                        mapping_found = True
                        break

                elif (start_diff >= 0): # seed start right of (or same as) mapping start
                    # case 2
                    if (start_diff > mapping["range"]):
                        continue

                    # case 3
                    elif (seed_range["range"] + start_diff <= mapping["range"]):
                        mapped_seed_ranges.append({ "from": mapping["to"] + start_diff, "range": seed_range["range"]}) # inside mapping

                        mapping_found = True
                        break

                    # case 5
                    else:
                        mapped_seed_ranges.append({"from": mapping["to"] + start_diff, "range": mapping["range"] - start_diff - 1}) # inside mapping
                        new_seed_ranges.append({"from": seed_range["from"] + (mapping["range"] - start_diff) + 1, "range": seed_range["range"] - (mapping["range"] - start_diff) - 1}) # right of mapping

                        mapping_found = True
                        break

            if (not mapping_found):
                mapped_seed_ranges.append(seed_range)

        if (self.verbose):
            print(f"Remaining Ranges: {new_seed_ranges}")

        return mapped_seed_ranges + (self.map_seed_ranges_recursively(map, new_seed_ranges) if len(new_seed_ranges) > 0 else [])