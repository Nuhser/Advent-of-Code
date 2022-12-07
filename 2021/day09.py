import aoc_util as aoc
import plotly.graph_objects as go

from math import prod

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.height_map = {(x, y): height for y, line in enumerate(aoc.parse_input(puzzle_input)) for x, height in enumerate(aoc.split_string_in_chunks(line, 1, cast_to=int))}
        self.height_map_for_visualization = [aoc.split_string_in_chunks(line, 1, cast_to=int) for line in aoc.parse_input(puzzle_input)]

    def part1(self) -> tuple[str, (int | str)]:
        # find low points and calculate risk level
        risk_levels = []
        for point in self.height_map:
            if all(self.height_map[point] < self.height_map[neighbour] for neighbour in self.get_neighbours(*point)):
                risk_levels.append(self.height_map[point] + 1)

        solution = sum(risk_levels)
        return f'{len(risk_levels)} Low Points found...\nTotal Risk Level: {solution}', solution

    def part2(self) -> tuple[str, (int | str)]:
        # find low points
        low_points = []
        for point in self.height_map:
            if all(self.height_map[point] < self.height_map[neighbour] for neighbour in self.get_neighbours(*point)):
                low_points.append(point)

        # calculate basin sizes
        basins = [self.get_basin_size(point) for point in low_points]

        solution = prod(sorted(basins, reverse=True)[: 3])
        return f'{len(basins)} Basins found...\nSolution: {solution}', solution

    def visualize(self) -> None:
        x = list(range(len(self.height_map_for_visualization[0])))
        y = list(range(len(self.height_map_for_visualization)))

        fig = go.Figure(data=[go.Surface(z=self.height_map_for_visualization, x=x, y=y)])
        fig.update_layout(title='Cave Height Map', scene = dict(aspectratio=dict(x=1, y=1, z=0.25), xaxis_title="X", yaxis_title="Y", zaxis_title="Height"), autosize=False, width=1200, height=900, margin=dict(l=65, r=50, b=10, t=50))
        fig.show()

    def get_neighbours(self, x, y):
        return filter(lambda height: height in self.height_map, [(x-1, y), (x+1, y), (x, y-1), (x, y+1)])

    def get_basin_size(self, point: tuple[int, int]):
        if self.height_map[point] == 9:
            return 0
        else:
            del self.height_map[point]
            return 1 + sum(map(self.get_basin_size, self.get_neighbours(*point)))
