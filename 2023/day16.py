from enum import Enum
from typing import override
from utility.mapping import generate_map_with_coordinates, get_map_dimensions
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map: dict[tuple[int, int], Mirror] = generate_map_with_coordinates(aoc.parse_input(puzzle_input), Mirror)


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        energized_tiles: int = self.energize_tiles_for_beam(((0, 0), (1, 0)))

        return f"Number of energized tiles: {energized_tiles}", energized_tiles


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        """
        This solution isn't very smart but more of a brute force approach. It took ~1.90491s to compute.
        """

        max_energized_tiles: int = 0
        x_len, y_len = get_map_dimensions(self.map)

        for x in range(x_len):
            max_energized_tiles = max(max_energized_tiles, self.energize_tiles_for_beam(((x, 0), (0, 1))))
            max_energized_tiles = max(max_energized_tiles, self.energize_tiles_for_beam(((x, y_len - 1), (0, -1))))

        for y in range(y_len):
            max_energized_tiles = max(max_energized_tiles, self.energize_tiles_for_beam(((0, y), (1, 0))))
            max_energized_tiles = max(max_energized_tiles, self.energize_tiles_for_beam(((x_len - 1, y), (-1, 0))))

        return f"Largest number of energized tiles: {max_energized_tiles}", max_energized_tiles


    def energize_tiles_for_beam(self, start_beam: tuple[tuple[int, int], tuple[int, int]]) -> int:
        energized_tiles: set[tuple[int, int]] = set()
        beam_history: set[tuple[tuple[int, int], tuple[int, int]]] = {start_beam}
        beams: list[tuple[tuple[int, int], tuple[int, int]]] = [start_beam]

        while (len(beams) > 0):
            # get next beam from list
            beam: tuple[tuple[int, int], tuple[int, int]] = beams.pop()

            while (True):
                # energize current tile
                energized_tiles.add(beam[0])

                # reflect beam
                new_beam_directions: list[tuple[int, int]] = self.map[beam[0]].reflect_light(beam[1])

                # save new beam to list
                if (len(new_beam_directions) == 2) and ((beam[0][0] + new_beam_directions[1][0], beam[0][1] + new_beam_directions[1][1]) in self.map):
                    beams.append(((beam[0][0] + new_beam_directions[1][0], beam[0][1] + new_beam_directions[1][1]), new_beam_directions[1]))

                # get new location for current beam
                new_beam_location: tuple[int, int] = beam[0][0] + new_beam_directions[0][0], beam[0][1] + new_beam_directions[0][1]

                # check if new location is still in map
                if (new_beam_location not in self.map):
                    break

                # save new location and direction to beam
                beam = new_beam_location, new_beam_directions[0]

                if (beam in beam_history):
                    break
                else:
                    beam_history.add(beam)

        return len(energized_tiles)


class Mirror(Enum):
    NONE = "."
    LEFT_RIGHT = "/"
    RIGHT_LEFT = "\\"
    H_SPLITTER = "-"
    V_SPLITTER = "|"

    def __str__(self) -> str:
        return self._value_

    def reflect_light(self, beam_direction: tuple[int, int]) -> list[tuple[int, int]]:
        match self:
            case Mirror.NONE:
                return [beam_direction]

            case Mirror.LEFT_RIGHT:
                beam_identity: int = sum(beam_direction)
                return [(beam_direction[0] + (-1 * beam_identity), beam_direction[1] + (-1 * beam_identity))]

            case Mirror.RIGHT_LEFT:
                return [(beam_direction[1], beam_direction[0])]

            case Mirror.H_SPLITTER:
                if (beam_direction[1] == 0):
                    return [beam_direction]
                else:
                    return [(1, 0), (-1, 0)]

            case Mirror.V_SPLITTER:
                if (beam_direction[0] == 0):
                    return [beam_direction]
                else:
                    return [(0, 1), (0, -1)]
                
            case _:
                raise ValueError(f"ERROR: Illegal mirror type '{self.name}'")