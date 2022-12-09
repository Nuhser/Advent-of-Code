import aoc_util as aoc

from operator import add

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.steps = []
        for direction, length in aoc.parse_input(puzzle_input, " "):
            match direction:
                case "U":
                    self.steps.append([[0, 1], int(length)])
                case "D":
                    self.steps.append([[0, -1], int(length)])
                case "R":
                    self.steps.append([[1, 0], int(length)])
                case "L":
                    self.steps.append([[-1, 0], int(length)])

    def part1(self) -> tuple[str, (int | str | None)]:
        # initialize knots
        knots = [[0, 0], [0, 0]]

        # move rope
        visited_locations = self.move_rope(knots)

        if self.verbose:
            visited_location_string = "\n".join(f"[{x}, {y}]" for x, y in visited_locations)
            print(f"\nVisited Locations:\n{visited_location_string}\n")

        return f"The tail of the rope visited {len(visited_locations)} locations.", len(visited_locations)

    def part2(self) -> tuple[str, (int | str | None)]:
        # initialize knots
        knots = [[0, 0] for _ in range(10)]

        # move rope
        visited_locations = self.move_rope(knots)

        if self.verbose:
            visited_location_string = "\n".join(f"[{x}, {y}]" for x, y in visited_locations)
            print(f"\nVisited Locations:\n{visited_location_string}\n")

        return f"The tail of the rope visited {len(visited_locations)} locations.", len(visited_locations)

    def move_rope(self, knots: list[list[int]]) -> set[tuple[int, int]]:
        # initialize visitied locations
        visited_locations = set()
        visited_locations.add((0, 0))

        # move rope
        for direction, length in self.steps:
            for _ in range(length):
                # move head
                knots[0] = list(map(add, knots[0], direction))

                # move tail if needed
                for i in range(len(knots) - 1):
                    if not self.are_knots_touching(knots[i], knots[i+1]):
                        if knots[i][0] > knots[i+1][0]:
                            knots[i+1][0] += 1
                        elif knots[i][0] < knots[i+1][0]:
                            knots[i+1][0] -= 1
                        
                        if knots[i][1] > knots[i+1][1]:
                            knots[i+1][1] += 1
                        elif knots[i][1] < knots[i+1][1]:
                            knots[i+1][1] -= 1

                visited_locations.add((knots[-1][0], knots[-1][1]))

                if self.verbose:
                    print(f"Tail Location: {knots[-1]}")

        return visited_locations

    def are_knots_touching(self, knot1: list[int], knot2: list[int]) -> bool:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (knot1[0] + x == knot2[0]) and (knot1[1] + y == knot2[1]):
                    return True
        
        return False