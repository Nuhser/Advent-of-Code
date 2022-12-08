import aoc_util as aoc

from math import prod

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.tree_map = {(x, y): self.Tree(height) for y, line in enumerate(aoc.parse_input(puzzle_input)) for x, height in enumerate(aoc.split_string_in_chunks(line, 1, cast_to=int))}

        self.max_x = 0
        self.max_y = 0
        for x, y in self.tree_map:
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    def part1(self) -> tuple[str, (int | str | None)]:
        for x, y in self.tree_map:
            if (x == 0) or (x == self.max_x) or (y == 0) or (y == self.max_y):
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the right
            visible = True
            for x2 in range(x+1, self.max_x+1):
                if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the left
            visible = True
            for x2 in range(x-1, -1, -1):
                if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the bottom
            visible = True
            for y2 in range(y+1, self.max_y+1):
                if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the top
            visible = True
            for y2 in range(y-1, -1, -1):
                if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

        solution = len([self.tree_map[x, y] for x, y in self.tree_map if self.tree_map[x, y].visible])
        return f"Number of visible trees: {solution}", solution

    def part2(self) -> tuple[str, (int | str | None)]:
        for y in range(self.max_y + 1):
            # calculate west view distance
            for x in range(self.max_x + 1):
                if x == 0:
                    continue

                x2 = x - 1
                while x2 >= 0:
                    self.tree_map[x, y].view_distance["west"] += 1

                    if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                        break

                    x2 -= 1

            # calculate east view distance
            for x in range(self.max_x, -1, -1):
                if x == self.max_x:
                    continue

                x2 = x + 1
                while x2 <= self.max_x:
                    self.tree_map[x, y].view_distance["east"] += 1

                    if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                        break

                    x2 += 1

        for x in range(self.max_x + 1):
            # calculate north view distance
            for y in range(self.max_y + 1):
                if y == 0:
                    continue

                y2 = y - 1
                while y2 >= 0:
                    self.tree_map[x, y].view_distance["north"] += 1

                    if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                        break

                    y2 -= 1

            # calculate south view distance
            for y in range(self.max_y, -1, -1):
                if y == self.max_y:
                    continue

                y2 = y + 1
                while y2 <= self.max_y:
                    self.tree_map[x, y].view_distance["south"] += 1

                    if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                        break

                    y2 += 1

        if self.verbose:
            print(f"Tree Map:\n{self.tree_map}")

        solution = max([prod(self.tree_map[tree].view_distance.values()) for tree in self.tree_map])
        return f"Highest scenic score: {solution}", solution

    class Tree:
        def __init__(self, height) -> None:
            self.height = height
            self.visible = False
            self.view_distance = {
                "north": 0,
                "south": 0,
                "west": 0,
                "east": 0
            }

        def __repr__(self) -> str:
            return f"Tree(height: {self.height}, visible: {self.visible}, view_distance: {self.view_distance})"