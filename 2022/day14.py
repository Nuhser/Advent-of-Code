import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    ROCK_STR = "█"
    SAND_STR = "▒"

    def parse(self, puzzle_input: list[str]) -> None:
        self.map: dict[tuple[int, int], str] = {(500, 0): "o"}

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

        x_keys = [x for x, _ in self.map.keys()]
        y_keys = [y for _, y in self.map.keys()]

        self.x_min = min(x_keys)
        self.x_max = max(x_keys)
        self.y_min = min(y_keys)
        self.y_max = max(y_keys)

        if self.verbose:
            for y in range(self.y_min, self.y_max + 1):
                print("".join([self.map[x, y] if (x, y) in self.map else " " for x in range(self.x_min, self.x_max + 1)]))

    def part1(self) -> tuple[str, (int | float | str | None)]:
        sand_counter = 0
        while True:
            x, y = (500, 0)
            landed = False

            while (x in range(self.x_min, self.x_max + 1)) and (y in range(self.y_min, self.y_max + 1)):
                if (x, y + 1) not in self.map:
                    y += 1
                elif (x - 1, y + 1) not in self.map:
                    x -= 1
                    y += 1
                elif (x + 1, y + 1) not in self.map:
                    x += 1
                    y += 1
                else:
                    self.map[x, y] = self.SAND_STR
                    landed = True
                    sand_counter += 1
                    break

            if not landed:
                break

        if self.verbose:
            for y in range(self.y_min, self.y_max + 1):
                print("".join([self.map[x, y] if (x, y) in self.map else " " for x in range(self.x_min, self.x_max + 1)]))

        return f"{sand_counter} sand units landed.", sand_counter

    def part2(self) -> tuple[str, (int | float | str | None)]:
        self.y_max += 2

        sand_counter = 0
        while True:
            x, y = (500, 0)

            while True:
                hit_gound = y >= self.y_max - 1
                if not hit_gound and ((x, y + 1) not in self.map):
                    y += 1
                elif not hit_gound and ((x - 1, y + 1) not in self.map):
                    x -= 1
                    y += 1
                elif not hit_gound and ((x + 1, y + 1) not in self.map):
                    x += 1
                    y += 1
                else:
                    self.map[x, y] = self.SAND_STR
                    self.x_min = min(self.x_min, x)
                    self.x_max = max(self.x_max, x)
                    sand_counter += 1
                    break

            if (x, y) == (500, 0):
                break

        if self.verbose:
            for y in range(self.y_min, self.y_max + 1):
                print("".join([self.map[x, y] if (x, y) in self.map else " " for x in range(self.x_min, self.x_max + 1)]))

        return f"{sand_counter} sand units landed.", sand_counter

    def visualize(self) -> None:
        import matplotlib.pyplot as plt

        map_copy = self.map.copy()

        self.part1()
        cave_image1 = []
        for y in range(self.y_min, self.y_max + 2):
            cave_image1.append([])
            for x in range(self.x_min, self.x_max + 1):
                if (x, y) in self.map:
                    cave_image1[-1].append([66, 135, 245] if self.map[x, y] == self.ROCK_STR else ([255, 0, 0] if self.map[x, y] == "o" else [252, 252, 144]))
                else:
                    cave_image1[-1].append([0, 0, 0])

        self.map = map_copy

        self.part2()
        cave_image2 = []
        for y in range(self.y_min, self.y_max):
            cave_image2.append([])
            for x in range(self.x_min, self.x_max + 1):
                if (x, y) in self.map:
                    cave_image2[-1].append([66, 135, 245] if self.map[x, y] == self.ROCK_STR else [252, 252, 144])
                else:
                    cave_image2[-1].append([0, 0, 0])

        figure, axes = plt.subplots(1, 2, width_ratios=[1, 4.25])

        figure.tight_layout()
        figure.suptitle("Advent of Code Day 14")

        axes[0].imshow(cave_image1)
        axes[0].axis("off")
        axes[0].set_title("Part 1")

        axes[1].imshow(cave_image2)
        axes[1].axis("off")
        axes[1].set_title("Part 2")

        plt.show()