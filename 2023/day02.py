import aoc_util as aoc

from typing import override


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        records = aoc.parse_input(
            [line.split(": ")[1] for line in puzzle_input],
            "; ", ", "
        )

        self.games = []
        for game in records:
            self.games.append({"red": [], "green": [], "blue": []})
            for draw in game:
                for color in draw:
                    self.games[-1][color.split(" ")[1]].append(int(color.split(" ")[0]))

        if (self.verbose):
            print(f"Game Records: {self.games}")


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        red = 12
        green = 13
        blue = 14

        possible_games = []
        for idx, game in enumerate(self.games):
            if (red >= max(game["red"])) and (green >= max(game["green"])) and (blue >= max(game["blue"])):
                possible_games.append(idx + 1)

        return f"Possible Games: {", ".join(str(id) for id in possible_games)}\nSum of IDs: {sum(possible_games)}", sum(possible_games)


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        raise NotImplementedError(f"Part 2 of the solution for day {self.day} of year {self.year} isn't implemented yet!")