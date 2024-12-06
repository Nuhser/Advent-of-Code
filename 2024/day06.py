from enum import Enum
from typing import override
import aoc_util as aoc
import utility.mapping as mapping


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map: dict[tuple[int, int], MapField] = mapping.generate_map_with_coordinates(aoc.parse_input(puzzle_input), MapField)
        self.guard_starting_position: tuple[int, int]

        for coords, map_field in self.map.items():
            if (map_field == MapField.GUARD_STARTING_POSITION):
                self.guard_starting_position = coords
                self.map[coords] = MapField.EMPTY
                break


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        guard_direction: tuple[int, int] = (0, -1)
        guard_x, guard_y = self.guard_starting_position

        visited_positions: set[tuple[int, int]] = {(guard_x, guard_y)}
        while (True):
            if (guard_direction[0] != 0): # moving horizontal
                coords, path = map(
                    list,
                    zip(*mapping.get_map_row(self.map, guard_y)[(guard_x + guard_direction[0])::guard_direction[0]])
                )
            else: # moving vertical
                coords, path = map(
                    list,
                    zip(*mapping.get_map_column(self.map, guard_x)[(guard_y + guard_direction[1])::guard_direction[1]])
                )

            try:
                distance_to_obstruction: int = path.index(MapField.OBSTRUCTION)

                # move guard
                for position in [
                    (guard_x + (guard_direction[0] * i), guard_y + (guard_direction[1] * i))
                    for i in range(1, (distance_to_obstruction + 1))
                ]:
                    visited_positions.add(position)

                guard_x += guard_direction[0] * distance_to_obstruction
                guard_y += guard_direction[1] * distance_to_obstruction

                # change direction
                match (guard_direction):
                    case (0, -1):
                        guard_direction = (1, 0)
                    case (1, 0):
                        guard_direction = (0, 1)
                    case (0, 1):
                        guard_direction = (-1, 0)
                    case (-1, 0):
                        guard_direction = (0, -1)

            except ValueError:
                # no obstruction in the path; guard leaves map
                for coord in coords:
                    visited_positions.add(coord)
                break

        return f"Guard visited {len(visited_positions)} positions on the map.", len(visited_positions)


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        return super().part2()
    

class MapField(Enum):
    EMPTY = "."
    OBSTRUCTION = "#"
    GUARD_STARTING_POSITION = "^"