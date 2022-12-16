import aoc_util as aoc
import json
from utility.path_finding import is_in_manhattan_distance

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.sensors: dict[tuple[int, int], int] = dict()
        self.beacons: set[tuple[int, int]] = set()

        for line in aoc.parse_input(puzzle_input, ": ", ", "):
            sensor_x = int(line[0][0].removeprefix("Sensor at x="))
            sensor_y = int(line[0][1].removeprefix("y="))
            beacon_x = int(line[1][0].removeprefix("closest beacon is at x="))
            beacon_y = int(line[1][1].removeprefix("y="))

            self.beacons.add((beacon_x, beacon_y))
            self.sensors[sensor_x, sensor_y] = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        if self.verbose:
            print(f"Sensors:\n{json.dumps(self.sensors, indent=2)}\n")

    def part1(self) -> tuple[str, (int | float | str | None)]:
        inspection_row = 10 if self.is_test else 2_000_000

        points: set[int, int] = set()
        for (x, y), distance in self.sensors.items():
            if inspection_row not in range(y - distance, y + distance + 1):
                continue

            x_min = x - (distance - abs(inspection_row - y))
            x_max = x + (distance - abs(inspection_row - y))

            for x in range(x_min, x_max + 1):
                if (x, inspection_row) not in self.beacons:
                    points.add(x)

        return f"{len(points)} points are covered by at least one beacon in row {inspection_row}.", len(points)

    def visualize(self) -> None:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        from matplotlib.patches import Polygon

        sensors_x = []
        sensors_y = []
        distances = []
        beacons_x = []
        beacons_y = []

        for (x, y), distance in self.sensors.items():
            sensors_x.append(x)
            sensors_y.append(y)
            distances.append(distance)

        for beacon in self.beacons:
            beacons_x.append(beacon[0])
            beacons_y.append(beacon[1])

        figure, ax = plt.subplots(dpi=300)

        ax.plot(sensors_x, sensors_y, "o", label="Sensors")
        ax.plot(beacons_x, beacons_y, "o", marker="$\U0001f4e1$", label="Beacons")
        line = ax.axhline(y=2_000_000, color="red", linestyle=":")

        ax.set_xlim(min(sensors_x + beacons_x) - 1e5, max(sensors_x + beacons_x) + 1e5)
        ax.set_ylim(min(sensors_y + beacons_y) - 1e5, max(sensors_y + beacons_y) + 1e5)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title("Advent of Code Day 15\nSensors searching nearest Beacons")
        figure.legend()

        n_frames = 300
        frame_time = 100
        frames: list[list[Polygon]] = []

        magic_number = min(distances) // 10
        for i in range(n_frames):
            patches = []
            for idx, distance in enumerate(distances):
                patch = ax.add_patch(Polygon(
                    [
                        [sensors_x[idx], sensors_y[idx] + ((magic_number * i) % distance)],
                        [sensors_x[idx] + ((magic_number * i) % distance), sensors_y[idx]],
                        [sensors_x[idx], sensors_y[idx] - ((magic_number * i) % distance)],
                        [sensors_x[idx] - ((magic_number * i) % distance), sensors_y[idx]]
                    ],
                    color="yellow",
                    alpha=0.5
                ))
                patch.set_visible(False)
                patches.append(patch)

            frames.append(patches)

        def init():
            print()
            return line,

        def animate(i):
            if i > 0:
                for patch in frames[i - 1]:
                    patch.set_visible(False)

            for patch in frames[i]:
                patch.set_visible(True)

            return line,

        animation = FuncAnimation(figure, animate, init_func=init, frames=n_frames, interval=frame_time, blit=True)
        animation.save(
            "2022/visualization15.gif",
            progress_callback=lambda i, n: print(f"{aoc.ANSI_LINE_BEGINNING}Animating frame {i + 1} of {n}..." + ("\nAnimation done. Saving GIF..." if (i+1) == n else ""))
        )
