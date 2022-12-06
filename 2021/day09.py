import aoc_util as aoc
import plotly.graph_objects as go

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.height_map = [aoc.split_string_in_chunks(line, 1, cast_to=int) for line in aoc.parse_input(puzzle_input)]

    def part1(self) -> str:
        x = list(range(len(self.height_map[0])))
        y = list(range(len(self.height_map)))

        fig = go.Figure(data=[go.Surface(z=self.height_map, x=x, y=y)])
        fig.update_layout(title='Cave Height Map', scene = dict(aspectratio=dict(x=1, y=1, z=0.25), xaxis_title="X", yaxis_title="Y", zaxis_title="Height"), autosize=False, width=700, height=600, margin=dict(l=65, r=50, b=10, t=50))
        fig.show()

        return ""

    def part2(self) -> str:
        return ""
