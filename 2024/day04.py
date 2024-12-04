from typing import override
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.puzzle_input: dict[tuple[int, int], str] = mapping.generate_map_with_coordinates(aoc.parse_input(puzzle_input))


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        words_found: int = 0

        for coords, letter in self.puzzle_input.items():
            if (letter != "X"):
                continue

            # print(f"Found X at {coords}")

            letter_m_list = mapping.get_matching_neighbors(
                self.puzzle_input,
                coords,
                lambda _, n: n[1] == "M"
            )

            # print(f"Found following Ms: {letter_m_list}")

            for (x, y), _ in letter_m_list:
                (dx, dy) = (x - coords[0], y - coords[1])

                # print(f"Direction: {(dx, dy)}")

                try:
                    if (self.puzzle_input[(x + dx), (y + dy)] == "A") and (self.puzzle_input[(x + 2 * dx), (y + 2 * dy)] == "S"):
                        words_found += 1
                except KeyError:
                    pass

            # break

        return f"Words found: {words_found}", words_found


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()