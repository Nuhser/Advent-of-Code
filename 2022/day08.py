import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.tree_map = {(x, y): [height, False] for y, line in enumerate(aoc.parse_input(puzzle_input)) for x, height in enumerate(aoc.split_string_in_chunks(line, 1, cast_to=int))}

        self.max_x = 0
        self.max_y = 0
        for x, y in self.tree_map:
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    def part1(self) -> tuple[str, (int | str | None)]:
        for x, y in self.tree_map:
            if (x == 0) or (x == self.max_x) or (y == 0) or (y == self.max_y):
                self.tree_map[x, y][1] = True
                continue

            # check if visible from the right
            visible = True
            for x2 in range(x+1, self.max_x+1):
                if self.tree_map[x2, y][0] >= self.tree_map[x, y][0]:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y][1] = True
                continue

            # check if visible from the left
            visible = True
            for x2 in range(x-1, -1, -1):
                if self.tree_map[x2, y][0] >= self.tree_map[x, y][0]:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y][1] = True
                continue

            # check if visible from the bottom
            visible = True
            for y2 in range(y+1, self.max_y+1):
                if self.tree_map[x, y2][0] >= self.tree_map[x, y][0]:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y][1] = True
                continue

            # check if visible from the top
            visible = True
            for y2 in range(y-1, -1, -1):
                if self.tree_map[x, y2][0] >= self.tree_map[x, y][0]:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y][1] = True
                continue

        solution = len([self.tree_map[x, y] for x, y in self.tree_map if self.tree_map[x, y][1]])
        return f"Number of visible trees: {solution}", solution