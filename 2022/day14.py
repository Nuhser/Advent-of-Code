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
        import numpy as np

        from matplotlib.animation import FuncAnimation

        # make map compatible with pyplot
        self.map = {coordinates: 1 if (self.map[coordinates] == self.ROCK_STR) else 2 for coordinates in self.map if self.map[coordinates] != "o"}        
        cave_image = np.array([[([46, 46, 46] if ((x, y) in self.map) else [0, 0, 0]) for x in range(self.x_min, self.x_max + 1)] for y in range(self.y_min, self.y_max + 1)])

        # initialize plot
        figure = plt.figure(figsize=[5, 10])

        # initialize image
        axes = plt.axes()
        axes.axis("off")
        axes.set_title("Advent of Code Day 14 Part 1 - Sand Falling")

        # add layers
        background = axes.imshow(cave_image)
        axes.plot([500 - self.x_min], [0], "o", ms=3, color="r")
        sand, = axes.plot([], [], "o", ms=3, color="y")

        # get sand history
        history = []

        sand_counter = 0
        while True:
            x, y = (500, 0)
            landed = False

            while (x in range(self.x_min, self.x_max + 1)) and (y in range(self.y_min, self.y_max + 1)):
                history.append((self.map, (x, y), sand_counter))
                if (x, y + 1) not in self.map:
                    y += 1
                elif (x - 1, y + 1) not in self.map:
                    x -= 1
                    y += 1
                elif (x + 1, y + 1) not in self.map:
                    x += 1
                    y += 1
                else:
                    self.map[x, y] = 2
                    landed = True
                    sand_counter += 1
                    break

            history.append((self.map, None, sand_counter))

            if not landed:
                break

        # set frame length and number of frames
        frame_length = 3
        n_frames = len(history)
        n_frames += (3000 // frame_length)

        def init():
            print()
            return background,

        def animate(i):
            if (i == 0) or (history[i][0] != history[i - 1][0]):
                background.set_data(np.array(
                    [
                        [
                            (
                                (
                                    [46, 46, 46]
                                    if self.map[x, y] == 1
                                    else [255, 255, 0]
                                )
                                if ((x, y) in self.map)
                                else [0, 0, 0]
                            )
                            for x in range(self.x_min, self.x_max + 1)
                        ] for y in range(self.y_min, self.y_max + 1)
                    ]
                ))

            if (i == 0) or (history[i][1] != history[i - 1][1]):
                if history[i][1] == None:
                    sand.set_data([], [])
                else:
                    sand.set_data([history[i][1][0]], [history[i][1][1]])

            if (i == 0) or (history[i][2] != history[i - 1][2]):
                axes.set_title(f"Advent of Code Day 14 Part 1 - Sand #{history[i][2]} Falling")

            return background,

        anim = FuncAnimation(figure, animate, init_func=init, frames=n_frames, interval=frame_length, blit=True)
        anim.save(
            "2022/visualization14.gif",
            progress_callback=lambda i, n: print(f"{aoc.ANSI_LINE_BEGINNING}Animating frame {i + 1} of {n}..." + ("\nAnimation done. Saving GIF..." if (i+1) == n else "")),
        )