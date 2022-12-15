import aoc_util as aoc
import json

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.sensors = [
            {
                "x": int(line[0][0].removeprefix("Sensor at x=")),
                "y": int(line[0][1].removeprefix("y=")),
                "beacon": {
                    "x": int(line[1][0].removeprefix("closest beacon is at x=")),
                    "y": int(line[1][1].removeprefix("y="))
                }
            }
            for line in aoc.parse_input(puzzle_input, ": ", ", ")
        ]

        for sensor in self.sensors:
            sensor["distance"] = abs(sensor["x"] - sensor["beacon"]["x"]) + abs(sensor["y"] - sensor["beacon"]["y"])

        if self.verbose:
            print(f"Sensors:\n{json.dumps(self.sensors, indent=2)}\n")