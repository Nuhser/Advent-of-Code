import aoc_util as aoc
import numpy as np
import plotly.graph_objects as go

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.start = (-1, -1)
        self.end = (-1, -1)
        self.heightmap: dict[tuple[int, int], int] = dict()
        for y, line in enumerate(aoc.parse_input(puzzle_input)):
            for x, height in enumerate(aoc.split_string_in_chunks(line, 1)):
                if height == "S":
                    self.start = (x, y)
                    height = "a"
                elif height == "E":
                    self.end = (x, y)
                    height = "z"

                self.heightmap[x, y] = ord(height) - ord("a")

        self.x_max = max([key[0] for key in self.heightmap.keys()])
        self.y_max = max([key[1] for key in self.heightmap.keys()])

    def part1(self) -> tuple[str, (int | float | str | None)]:
        weight_map_uphill = {coordinates: [(point, 1) for point in self.get_adjacent_points(*coordinates)] for coordinates in self.heightmap.keys()}
        _, costs = aoc.calculate_dijkstra(weight_map_uphill, self.start, self.end)

        return f"Shortest path takes {aoc.ANSI_UNDERLINE + str(costs[self.end]) + aoc.ANSI_NOT_UNDERLINE} steps from {self.start} to {self.end}.", costs[self.end]

    def part2(self) -> tuple[str, (int | float | str | None)]:
        weight_map_downhill = {coordinates: [(point, 1) for point in self.get_adjacent_points(*coordinates, False)] for coordinates in self.heightmap.keys()}
        _, costs = aoc.calculate_dijkstra(weight_map_downhill, self.end)

        shortest_path_start = None
        shortest_path_costs = float("inf")
        for point in costs:
            if (self.heightmap[point] == 0) and (costs[point] < shortest_path_costs):
                shortest_path_costs = costs[point]
                shortest_path_start = point

        return f"Shortest path takes {aoc.ANSI_UNDERLINE + str(shortest_path_costs) + aoc.ANSI_NOT_UNDERLINE} steps from {shortest_path_start} to {self.end}.", shortest_path_costs

    def visualize(self) -> None:
        # calculate shortest path for part 1 with dijkstra
        weight_map_uphill = {coordinates: [(point, 1) for point in self.get_adjacent_points(*coordinates)] for coordinates in self.heightmap.keys()}
        parents_map_part1, _ = aoc.calculate_dijkstra(weight_map_uphill, self.start, self.end)

        shortest_path_part1 = [self.end]
        _point = self.end
        while _point != self.start:
            shortest_path_part1.append(parents_map_part1[_point])
            _point = parents_map_part1[_point]

        # calculate shortest path for part 1 with dijkstra
        weight_map_downhill = {coordinates: [(point, 1) for point in self.get_adjacent_points(*coordinates, False)] for coordinates in self.heightmap.keys()}
        parents_map_part2, costs_part2 = aoc.calculate_dijkstra(weight_map_downhill, self.end)

        shortest_path_start_part2 = None
        shortest_path_costs_part2 = float("inf")
        for point in costs_part2:
            if (self.heightmap[point] == 0) and (costs_part2[point] < shortest_path_costs_part2):
                shortest_path_costs_part2 = costs_part2[point]
                shortest_path_start_part2 = point

        shortest_path_part2 = [shortest_path_start_part2]
        _point = shortest_path_start_part2
        while _point != self.end:
            shortest_path_part2.append(parents_map_part2[_point])
            _point = parents_map_part2[_point]

        # get arrays for height map
        z = [[self.heightmap[_x, _y] for _x in range(self.x_max + 1)] for _y in range(self.y_max + 1)]
        x = list(range(len(z[0])))
        y = list(range(len(z)))
        
        # add height map surface
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale="Greens")])

        # add start and end point
        fig.add_scatter3d(
            x = [self.start[0], shortest_path_start_part2[0], self.end[0]],
            y = [self.start[1], shortest_path_start_part2[1], self.end[1]],
            z = [self.heightmap[self.start], self.heightmap[shortest_path_start_part2], self.heightmap[self.end]],
            showlegend = False,
            mode = "markers",
            marker = dict(
                size = 10,
                color = [0, 0, 0],
                colorscale = "Plotly3"
            )
        )

        # add line from start to end for part 1
        fig.add_scatter3d(
            x = [x for x, _ in shortest_path_part1],
            y = [y for _, y in shortest_path_part1],
            z = [self.heightmap[point] for point in shortest_path_part1],
            name = "Part 1",
            mode = "lines",
            line = dict(width=8)
        )

        # add line from start to end for part 2
        fig.add_scatter3d(
            x = [x for x, _ in shortest_path_part2],
            y = [y for _, y in shortest_path_part2],
            z = [self.heightmap[point] for point in shortest_path_part2],
            name = "Part 2",
            mode = "lines",
            line = dict(width=8)
        )
        
        # add title and set layout
        fig.update_layout(
            title = "Mountain Height Map",
            scene = dict(
                aspectratio = dict(x=1, y=(self.y_max / self.x_max), z=0.25),
                xaxis_title = "X",
                yaxis_title = "Y",
                zaxis_title = "Height",
                annotations = [
                    dict(
                        showarrow=True,
                        x = self.start[0],
                        y = self.start[1],
                        z = self.heightmap[self.start],
                        text = "Start (Part 1)",
                        xanchor = "right",
                        yanchor = "bottom",
                        opacity = 0.7,
                        font = dict(
                            color = "red",
                            size = 20
                        ),
                        arrowcolor = "red",
                        arrowsize = 5,
                        arrowwidth = 0.5,
                        arrowhead = 2
                    ),
                    dict(
                        showarrow=True,
                        x = shortest_path_start_part2[0],
                        y = shortest_path_start_part2[1],
                        z = self.heightmap[shortest_path_start_part2],
                        text = "Start (Part 2)",
                        xanchor = "right",
                        yanchor = "bottom",
                        opacity = 0.7,
                        font = dict(
                            color = "red",
                            size = 20
                        ),
                        arrowcolor = "red",
                        arrowsize = 5,
                        arrowwidth = 0.5,
                        arrowhead = 2
                    ),
                    dict(
                        showarrow = True,
                        x = self.end[0],
                        y = self.end[1],
                        z = self.heightmap[self.end],
                        text = "End",
                        xanchor = "right",
                        yanchor = "bottom",
                        opacity = 0.7,
                        font = dict(
                            color = "red",
                            size = 20
                        ),
                        arrowcolor = "red",
                        arrowsize = 5,
                        arrowwidth = 0.5,
                        arrowhead = 2
                    )
                ]
            ),
            autosize = False,
            width = 2000,
            height = 1000,
            margin = dict(l=65, r=50, b=10, t=50),
            legend_orientation = "h"
        )

        fig.show()

    def get_adjacent_points(self, x: int, y: int, uphill: bool=True) -> list[tuple[int, int]]:
        adjecent_points = []

        if uphill:
            if ((x - 1) >= 0) and (self.heightmap[x - 1, y] <= (self.heightmap[x, y] + 1)):
                adjecent_points.append((x - 1, y))

            if ((x + 1) <= self.x_max) and (self.heightmap[x + 1, y] <= (self.heightmap[x, y] + 1)):
                adjecent_points.append((x + 1, y))

            if ((y - 1) >= 0) and (self.heightmap[x, y - 1] <= (self.heightmap[x, y] + 1)):
                adjecent_points.append((x, y - 1))

            if ((y + 1) <= self.y_max) and (self.heightmap[x, y + 1] <= (self.heightmap[x, y] + 1)):
                adjecent_points.append((x, y + 1))

        else:
            if ((x - 1) >= 0) and (self.heightmap[x - 1, y] >= (self.heightmap[x, y] - 1)):
                adjecent_points.append((x - 1, y))

            if ((x + 1) <= self.x_max) and (self.heightmap[x + 1, y] >= (self.heightmap[x, y] - 1)):
                adjecent_points.append((x + 1, y))

            if ((y - 1) >= 0) and (self.heightmap[x, y - 1] >= (self.heightmap[x, y] - 1)):
                adjecent_points.append((x, y - 1))

            if ((y + 1) <= self.y_max) and (self.heightmap[x, y + 1] >= (self.heightmap[x, y] - 1)):
                adjecent_points.append((x, y + 1))

        return adjecent_points