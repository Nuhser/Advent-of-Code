import aoc_util as aoc
import matplotlib.pyplot as plt
import numpy as np

from queue import PriorityQueue, Queue

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.points_single = {(x, y): [risk_level, float("inf"), None] for y, line in enumerate(aoc.parse_input(puzzle_input)) for x, risk_level in enumerate(aoc.split_string_in_chunks(line, 1, cast_to=int))}
        
        self.points_single[0, 0] = [self.points_single[0, 0][0], 0, None]
        self.target_single = (max(x for x, _ in self.points_single), max(y for _, y in self.points_single))

        self.points_multiple = dict()
        for y, line in enumerate(aoc.parse_input(puzzle_input)):
            for x, risk_level in enumerate(aoc.split_string_in_chunks(line, 1, cast_to=int)):
                for i in range(5):
                    for j in range(5):
                        self.points_multiple[(x + (100 * i), y + (100 * j))] = [(int(risk_level) - 1 + i + j) % 9 + 1, float('inf'), None]

        self.points_multiple[0, 0] = [self.points_multiple[0, 0][0], 0, None]
        self.target_multiple = (max(x for x, _ in self.points_multiple), max(y for _, y in self.points_multiple))

    def part1(self) -> tuple[str, (int | str)]:
        wait_list = [(0, 0)]
        completed_points = []

        while self.target_single not in completed_points:
            current_point = wait_list.pop(0)

            for neighbour in self.get_neighbours(*current_point):
                if neighbour not in completed_points:
                    new_cost = self.points_single[current_point][1] + self.points_single[neighbour][0]

                    if self.points_single[neighbour][1] > new_cost:
                        self.points_single[neighbour][1] = new_cost
                        self.points_single[neighbour][2] = current_point

                    if neighbour not in wait_list:
                        wait_list.append(neighbour)

            completed_points.append(current_point)

        return f'Lowest Risk Level: {self.points_single[self.target_single][1]}', int(self.points_single[self.target_single][1])

    def part2(self) -> tuple[str, (int | str)]:
        wait_list: Queue[tuple[int, int]] = PriorityQueue()
        wait_list.put((0, (0, 0)))
        completed_points = []

        while self.target_multiple not in completed_points:
            current_point = wait_list.get()[1]

            for neighbour in self.get_neighbours(*current_point):
                if neighbour not in completed_points:
                    new_cost = self.points_multiple[current_point][1] + self.points_multiple[neighbour][0]

                    if self.points_multiple[neighbour][1] > new_cost:
                        self.points_multiple[neighbour][1] = new_cost
                        self.points_multiple[neighbour][2] = current_point

                    # if neighbour not in wait_list:
                        wait_list.put((self.points_multiple[neighbour][1], neighbour))

            completed_points.append(current_point)

        solution = self.points_multiple[self.target_multiple][1]
        return f'Lowest Risk Level: {solution}', solution

    def visualize(self) -> None:
        self.part1()

        colors = {1: 'limegreen', 2: 'lightgreen', 3: 'yellowgreen', 4: 'darkkhaki', 5: 'gold', 6: 'orange', 7: 'darkorange', 8: 'orangered', 9: 'maroon'}
        x = np.array([point[0] for point in self.points_single])
        y = np.array([point[1] for point in self.points_single])
        x_path = []
        y_path = []

        pre_point = self.target_single
        while pre_point != None:
            x_path.append(pre_point[0])
            y_path.append(pre_point[1])
            pre_point = self.points_single[pre_point][2]

        plt.figure(figsize=(15, 15))
        plt.gca().invert_yaxis()

        risk_levels =[self.points_single[point][0] for point in self.points_single]
        for level in np.unique(risk_levels):
            idx = np.where(risk_levels == level)
            plt.scatter(x[idx], y[idx], c = colors[level], label = level, s = 45, alpha=0.7)

        if pre_point != self.target_single:
            plt.plot(x_path, y_path, 'm')

        plt.title('Path with Lowest Risk using Dijkstra')
        plt.legend()
        plt.show()

    def get_neighbours(self, x, y):
        return filter(lambda point: point in self.points_single, [(x-1, y), (x+1, y), (x, y-1), (x, y+1)])
