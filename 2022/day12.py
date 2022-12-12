import aoc_util as aoc
import numpy as np
import plotly.graph_objects as go
import prettytable

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

        if self.verbose:
            table = prettytable.PrettyTable()
            table.set_style(prettytable.DOUBLE_BORDER)
            table.int_format="02"
            table.align = "c"

            table.field_names = [""] + list(range(self.x_max + 1))

            for y in range(self.y_max + 1):
                table.add_row([y] + [self.heightmap[x, y] for x in range(self.x_max + 1)])

            print(table)

    def visualize(self) -> None:
        # get arrays for height map
        z = [[self.heightmap[_x, _y] for _x in range(self.x_max + 1)] for _y in range(self.y_max + 1)]
        x = list(range(len(z[0])))
        y = list(range(len(z)))
        
        # add height map surface
        fig = go.Figure(data = [go.Surface(z=z, x=x, y=y)])

        # add height lines to top and bottom of plot
        fig.update_traces(
            contours_z = dict(
                show = True,
                usecolormap = True,
                highlightcolor = "limegreen",
                project_z = True
            )
        )

        # add start and end point
        fig.add_scatter3d(
            x = [self.start[0], self.end[0]],
            y = [self.start[1], self.end[1]],
            z = [self.heightmap[self.start], self.heightmap[self.end]],
            mode = "markers",
            marker = dict(
                size = 10,
                color = [self.start[0], self.end[0]],
                colorscale = "Bluyl"
            )
        )
        
        # add title and set layout
        fig.update_layout(
            title = "Mountain Hight Map",
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
                        text = "Start",
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
            height = 1200,
            margin = dict(l=65, r=50, b=10, t=50)
        )

        fig.show()