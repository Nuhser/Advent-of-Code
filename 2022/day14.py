import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    ROCK_STR = "█"
    SAND_STR = "▒"

    def parse(self, puzzle_input: list[str]) -> None:
        self.map: dict[tuple[int, int], str] = {}

        for line in aoc.parse_input(puzzle_input, " -> ", ",", cast_to=int):
            for idx in range(len(line) - 1):
                x1, y1 = line[idx]
                x2, y2 = line[idx + 1]

                if x1 == x2:
                    if y1 < y2:
                        for y in range(y1, y2 + 1):
                            self.map[x1, y] = self.ROCK_STR
                    else:
                        for y in range(y2, y1 + 1):
                            self.map[x1, y] = self.ROCK_STR
                else:
                    if x1 < x2:
                        for x in range(x1, x2 + 1):
                            self.map[x, y1] = self.ROCK_STR
                    else:
                        for x in range(x2, x1 + 1):
                            self.map[x, y1] = self.ROCK_STR

        if self.verbose:
            print(self.map.keys())

        x_keys = [x for x, _ in self.map.keys()]
        y_keys = [y for _, y in self.map.keys()]

        self.x_min = min(x_keys)
        self.x_max = max(x_keys)
        self.y_min = min(y_keys)
        self.y_max = max(y_keys)

        if self.verbose:
            for y in range(self.y_min, self.y_max + 1):
                print("".join([self.map[x, y] if (x, y) in self.map else " " for x in range(self.x_min, self.x_max + 1)]))
