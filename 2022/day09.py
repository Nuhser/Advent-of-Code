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
        visited_locations, _ = self.move_rope(knots)

        return f"The tail of the rope visited {len(visited_locations)} locations.", len(visited_locations)

    def part2(self) -> tuple[str, (int | str | None)]:
        # initialize knots
        knots = [[0, 0] for _ in range(10)]

        # move rope
        visited_locations, _ = self.move_rope(knots)

        return f"The tail of the rope visited {len(visited_locations)} locations.", len(visited_locations)

    def visualize(self) -> None:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        
        # initialize knots
        knots = [[0, 0] for _ in range(10)]

        # move rope
        _, history = self.move_rope(knots, save_history=True)

        print(f"Need to animate {len(history)} frames.")

        # initialize plot
        fig = plt.figure()

        ax = plt.axes()
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_title(f"Rope Movement with 10 Knots")

        visited_points1, = ax.plot([], [], "-", lw=1, label="Part 1")
        visited_points2, = ax.plot([], [], "-", lw=1, label="Part 2")
        line, = ax.plot([], [], "-o", lw=2)
        head, = ax.plot([], [], "o", ms=10)

        ax.legend()

        # animation init function
        def init():
            print()

            visited_points1.set_data([0], [0])
            visited_points2.set_data([0], [0])
            line.set_data([0] * 10, [0] * 10)
            head.set_data([0], [0])

            return line,

        # animation function
        def animate(i):
            locations = history[i][0]

            x_visited1 = [x for x, _ in history[i][1][0]]
            y_visited1 = [y for _, y in history[i][1][0]]
            
            x_visited2 = [x for x, _ in history[i][1][1]]
            y_visited2 = [y for _, y in history[i][1][1]]

            x_locations = [x for x, _ in locations]
            y_locations = [y for _, y in locations]

            # calculate plot size
            ax.set_xlim(min(min(x_visited1), min(x_visited1), min(x_locations)) - 5, max(max(x_visited1), max(x_visited1), max(x_locations)) + 5)
            ax.set_ylim(min(min(y_visited1), min(y_visited1), min(y_locations)) - 5, max(max(y_visited1), max(x_visited1), max(y_locations)) + 5)

            # update plot title
            ax.set_title(f"Rope Movement with 10 Knots - Step {i+1} of {len(history)}")

            # draw points
            visited_points1.set_data(x_visited1, y_visited1)
            visited_points2.set_data(x_visited2, y_visited2)
            line.set_data(x_locations, y_locations)
            head.set_data(x_locations[0:1], y_locations[0:1])

            return line,

        anim = FuncAnimation(fig, animate, init_func=init, frames=len(history), interval=50, blit=True)

        anim.save(
            "2022/visualization09.gif",
            progress_callback=lambda i, n: print(f"{aoc.ANSI_LINE_BEGINNING}Animating frame {i + 1} of {n}..." + ("\nAnimation done. Saving GIF..." if (i+1) == n else ""))
        )

    def move_rope(self, knots: list[list[int]], save_history: bool=False) -> tuple[set[tuple[int, int]], (list[tuple[list[list[int]], list[list[int]]]] | None)]:
        # initialize visitied locations
        visited_locations = set()
        visited_locations.add((0, 0))

        # initialize history
        history = []
        if save_history:
            history = [([knot[:] for knot in knots], ([knots[1].copy()], [knots[-1].copy()]))]

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

                # update visited locations
                visited_locations.add((knots[-1][0], knots[-1][1]))

                # update history
                if save_history:
                    history.append(([knot[:] for knot in knots], (history[-1][1][0] + [knots[1].copy()], history[-1][1][1] + [knots[-1].copy()])))

                if self.verbose:
                    print(f"Tail Location: {knots[-1]}")

        if self.verbose:
            visited_location_string = "\n".join(f"[{x}, {y}]" for x, y in visited_locations)
            print(f"\nVisited Locations:\n{visited_location_string}\n")

        return visited_locations, (history if len(history) > 0 else None)

    def are_knots_touching(self, knot1: list[int], knot2: list[int]) -> bool:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (knot1[0] + x == knot2[0]) and (knot1[1] + y == knot2[1]):
                    return True
        
        return False