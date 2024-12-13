import aoc_util as aoc
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

from math import prod

import utility.util

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.tree_map = {(x, y): self.Tree(height) for y, line in enumerate(aoc.parse_input(puzzle_input)) for x, height in enumerate(utility.util.split_string_in_chunks(line, 1, cast_to=int))}

        self.max_x = 0
        self.max_y = 0
        for x, y in self.tree_map:
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)

    def part1(self) -> tuple[str, (int | str | None)]:
        for x, y in self.tree_map:
            if (x == 0) or (x == self.max_x) or (y == 0) or (y == self.max_y):
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the right
            visible = True
            for x2 in range(x+1, self.max_x+1):
                if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the left
            visible = True
            for x2 in range(x-1, -1, -1):
                if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the bottom
            visible = True
            for y2 in range(y+1, self.max_y+1):
                if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

            # check if visible from the top
            visible = True
            for y2 in range(y-1, -1, -1):
                if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                    visible = False
                    break

            if visible:
                self.tree_map[x, y].visible = True
                continue

        solution = len([self.tree_map[x, y] for x, y in self.tree_map if self.tree_map[x, y].visible])
        return f"Number of visible trees: {solution}", solution

    def part2(self) -> tuple[str, (int | str | None)]:
        for y in range(self.max_y + 1):
            # calculate west view distance
            for x in range(self.max_x + 1):
                if x == 0:
                    continue

                x2 = x - 1
                while x2 >= 0:
                    self.tree_map[x, y].view_distance["west"] += 1

                    if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                        break

                    x2 -= 1

            # calculate east view distance
            for x in range(self.max_x, -1, -1):
                if x == self.max_x:
                    continue

                x2 = x + 1
                while x2 <= self.max_x:
                    self.tree_map[x, y].view_distance["east"] += 1

                    if self.tree_map[x2, y].height >= self.tree_map[x, y].height:
                        break

                    x2 += 1

        for x in range(self.max_x + 1):
            # calculate north view distance
            for y in range(self.max_y + 1):
                if y == 0:
                    continue

                y2 = y - 1
                while y2 >= 0:
                    self.tree_map[x, y].view_distance["north"] += 1

                    if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                        break

                    y2 -= 1

            # calculate south view distance
            for y in range(self.max_y, -1, -1):
                if y == self.max_y:
                    continue

                y2 = y + 1
                while y2 <= self.max_y:
                    self.tree_map[x, y].view_distance["south"] += 1

                    if self.tree_map[x, y2].height >= self.tree_map[x, y].height:
                        break

                    y2 += 1

        if self.verbose:
            print(f"Tree Map:\n{self.tree_map}")

        solution = max([prod(self.tree_map[tree].view_distance.values()) for tree in self.tree_map])
        return f"Highest scenic score: {solution}", solution

    def visualize(self) -> None:
        _, visibile_trees = self.part1()
        _, max_scenic_score = self.part2()

        heights = np.array([[self.tree_map[x, y].height for x in range(self.max_x + 1)] for y in range(self.max_y + 1)])
        visibilities = np.array([[(1 if self.tree_map[x, y].visible else 0) for x in range(self.max_x + 1)] for y in range(self.max_y + 1)])
        scenic_scores = np.array([[prod(self.tree_map[x, y].view_distance.values()) for x in range(self.max_x + 1)] for y in range(self.max_y + 1)])

        _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

        ax2.axis("off")

        im = ax1.imshow(heights)
        cbar = plt.colorbar(im)
        cbar.ax.get_yaxis().labelpad = 15
        cbar.ax.set_ylabel("Height", rotation=270)
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])
        ax1.set_title("Tree Height Map")

        im = ax3.imshow(visibilities)
        ax3.set_xticklabels([])
        ax3.set_yticklabels([])
        ax3.set_title(f"Tree Visibility (Total Number: {visibile_trees})")

        im = ax4.imshow(scenic_scores, norm=colors.LogNorm())
        ax4.set_xticklabels([])
        ax4.set_yticklabels([])
        ax4.set_title(f"Scenic Scores (Highest Score: {max_scenic_score})")

        plt.show()

    class Tree:
        def __init__(self, height) -> None:
            self.height = height
            self.visible = False
            self.view_distance = {
                "north": 0,
                "south": 0,
                "west": 0,
                "east": 0
            }

        def __repr__(self) -> str:
            return f"Tree(height: {self.height}, visible: {self.visible}, view_distance: {self.view_distance})"