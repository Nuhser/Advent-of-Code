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

    class Tree:
        def __init__(self, height) -> None:
            self.height = height
            self.visible = False
            self.view_distance = [0, 0, 0, 0]
            self.scenic_view = 0