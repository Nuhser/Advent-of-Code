from typing import override
import aoc_util as aoc
import utility.mapping as mapping


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input: dict[tuple[int, int], str] = mapping.generate_map_with_coordinates(aoc.parse_input(puzzle_input))


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        xmas_found: int = 0

        for coords, letter in self.puzzle_input.items():
            if (letter != "X"):
                continue

            letter_m_list = mapping.get_matching_neighbors(
                self.puzzle_input,
                coords,
                lambda _, n: n[1] == "M"
            )

            for (x, y), _ in letter_m_list:
                (dx, dy) = (x - coords[0], y - coords[1])

                try:
                    if (self.puzzle_input[(x + dx), (y + dy)] == "A") and (self.puzzle_input[(x + 2 * dx), (y + 2 * dy)] == "S"):
                        xmas_found += 1
                except KeyError:
                    pass

        return f"Words found: {xmas_found}", xmas_found


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        xmas_found: int = 0

        for coords, letter in self.puzzle_input.items():
            # only look at As and their neighbors
            if (letter != "A"):
                continue

            # check if two Ms are neighboring diagonally
            letter_m_list = mapping.get_matching_neighbors(
                self.puzzle_input,
                coords,
                lambda _, neighbor: neighbor[1] == "M",
                horizontal=False,
                vertical=False
            )

            if (len(letter_m_list) != 2):
                continue

            # check if two Ss are neighboring diagonally
            letter_s_list = mapping.get_matching_neighbors(
                self.puzzle_input,
                coords,
                lambda _, neighbor: neighbor[1] == "S",
                horizontal=False,
                vertical=False
            )

            if (len(letter_s_list) != 2):
                continue

            # check if the two Ms are not diagonal two each other
            m_direction: tuple[int, int] = (0, 0)
            for (x, y), _ in letter_m_list:
                m_direction = (m_direction[0] + (x - coords[0]), m_direction[1] + (y - coords[1]))

            if (m_direction == (0, 0)):
                continue

            xmas_found += 1

        return f"XMASs found: {xmas_found}", xmas_found