import aoc_util as aoc
from numpy import sign

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.vent_lines = aoc.parse_input(puzzle_input, " -> ", ",", cast_to=int)

    def part1(self) -> str:
        # remove non horizontal or verticel lines
        vent_lines = [line for line in self.vent_lines if line[0][0] == line[1][0] or line[0][1] == line[1][1]]

        # fill map
        vent_map = dict()
        for line in vent_lines:
            # vertical line
            if (line[0][0] == line[1][0]):
                direction = sign(line[1][1] - line[0][1])
                for y in range(line[0][1], line[1][1] + direction, direction):
                    if (line[0][0], y) not in vent_map:
                        vent_map[(line[0][0], y)] = 1
                    else:
                        vent_map[(line[0][0], y)] += 1

            # horizontal line
            elif (line[0][1] == line[1][1]):
                direction = sign(line[1][0] - line[0][0])
                for x in range(line[0][0], line[1][0] + direction, direction):
                    if (x, line[0][1]) not in vent_map:
                        vent_map[(x, line[0][1])] = 1
                    else:
                        vent_map[(x, line[0][1])] += 1

            # Shouldn't hapen in this part of the challenge.
            else:
                return "ERROR: Line not horizontal or vertical"

        # count dangerous coords
        count = len([coord for coord in vent_map if vent_map[coord] > 1])

        return f'Solution: {count}'

    def part2(self) -> str:
        # fill map
        vent_map = dict()
        for line in self.vent_lines:
            # vertical line
            if (line[0][0] == line[1][0]):
                direction = sign(line[1][1] - line[0][1])
                for y in range(line[0][1], line[1][1] + direction, direction):
                    if (line[0][0], y) not in vent_map:
                        vent_map[(line[0][0], y)] = 1
                    else:
                        vent_map[(line[0][0], y)] += 1

            # horizontal line
            elif (line[0][1] == line[1][1]):
                direction = sign(line[1][0] - line[0][0])
                for x in range(line[0][0], line[1][0] + direction, direction):
                    if (x, line[0][1]) not in vent_map:
                        vent_map[(x, line[0][1])] = 1
                    else:
                        vent_map[(x, line[0][1])] += 1

            # diagonal lines
            else:
                x1, y1 = (line[0][0], line[0][1]) if line[0][0] < line[1][0] else (line[1][0], line[1][1])
                x2, y2 = (line[0][0], line[0][1]) if line[0][0] > line[1][0] else (line[1][0], line[1][1])
                gradient = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
                b = y1 - int(x1 * gradient)

                while True:
                    if (x1, y1) not in vent_map:
                        vent_map[(x1, y1)] = 1
                    else:
                        vent_map[(x1, y1)] += 1

                    x1 += 1
                    y1 = int(x1 * gradient) + b

                    if x1 == x2 and y1 == y2:
                        if (x1, y1) not in vent_map:
                            vent_map[(x1, y1)] = 1
                        else:
                            vent_map[(x1, y1)] += 1
                            
                        break

        # count dangerous coords
        count = len([coord for coord in vent_map if vent_map[coord] > 1])

        return f'Solution: {count}'
