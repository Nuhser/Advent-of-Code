from enum import Enum
from typing import override

import aoc_util as aoc
from utility.mapping import Map


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.map = Map(aoc.parse_input(puzzle_input), cast_to=MapField)

        # print(self.map.__dict__)

        guard_starting_position = self.map.find_coords(MapField.GUARD_STARTING_POSITION)

        self.guard_starting_position: tuple[int, int] = guard_starting_position
        self.map.set(guard_starting_position, MapField.EMPTY)

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        guard_direction: tuple[int, int] = (0, -1)
        guard_x, guard_y = self.guard_starting_position

        visited_positions: set[tuple[int, int]] = {(guard_x, guard_y)}
        while True:
            coords, distance_to_obstruction = (
                self.get_path_and_distance_to_next_obstruction(
                    self.map, (guard_x, guard_y), guard_direction
                )
            )

            if distance_to_obstruction == None:
                # no obstruction found; guard leaves map
                for coord in coords:
                    visited_positions.add(coord)
                break

            else:
                # move guard
                for position in [
                    (
                        guard_x + (guard_direction[0] * i),
                        guard_y + (guard_direction[1] * i),
                    )
                    for i in range(1, (distance_to_obstruction + 1))
                ]:
                    visited_positions.add(position)

                guard_x += guard_direction[0] * distance_to_obstruction
                guard_y += guard_direction[1] * distance_to_obstruction

                # change direction
                guard_direction = self.rotate_guard(guard_direction)

        return f"Guard visited {len(visited_positions)} positions on the map.", len(
            visited_positions
        )

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        guard_direction: tuple[int, int] = (0, -1)
        guard_x, guard_y = self.guard_starting_position

        visited_positions_with_directions: set[
            tuple[tuple[int, int], tuple[int, int]]
        ] = {((guard_x, guard_y), guard_direction)}
        loops_found: int = 0
        checked_obstruction_coords: set[tuple[int, int]] = set()

        while True:
            coords, distance_to_obstruction = (
                self.get_path_and_distance_to_next_obstruction(
                    self.map, (guard_x, guard_y), guard_direction
                )
            )

            if distance_to_obstruction == None:
                # no obstruction in the path; guard leaves map
                coord: tuple[int, int]
                for i, coord in enumerate(coords):
                    if (not coord in checked_obstruction_coords) and (
                        self.check_path_for_loops(
                            visited_positions_with_directions,
                            (
                                guard_x + (i * guard_direction[0]),
                                guard_y + (i * guard_direction[1]),
                            ),
                            guard_direction,
                            coord,
                        )
                    ):
                        loops_found += 1

                    checked_obstruction_coords.add(coord)
                break

            else:
                # move guard
                for position in [
                    (
                        guard_x + (guard_direction[0] * i),
                        guard_y + (guard_direction[1] * i),
                    )
                    for i in range(1, (distance_to_obstruction + 1))
                ]:
                    if (not position in checked_obstruction_coords) and (
                        self.check_path_for_loops(
                            visited_positions_with_directions,
                            (guard_x, guard_y),
                            guard_direction,
                            position,
                        )
                    ):
                        loops_found += 1

                    checked_obstruction_coords.add(position)

                    visited_positions_with_directions.add((position, guard_direction))

                    guard_x += guard_direction[0]
                    guard_y += guard_direction[1]

                # change direction
                guard_direction = self.rotate_guard(guard_direction)

        return f"Possible loops found: {loops_found}", loops_found

    def get_path_and_distance_to_next_obstruction(
        self,
        obstructions_map: Map["MapField"],
        current_position: tuple[int, int],
        current_direction: tuple[int, int],
    ) -> tuple[list[tuple[int, int]], (int | None)]:

        coords: list[tuple[int, int]]
        path: list[MapField]

        if current_direction[0] != 0:  # moving horizontal
            coords, path = map(
                list,
                zip(
                    *obstructions_map.get_row(current_position[1])[
                        (
                            current_position[0] + current_direction[0]
                        ) :: current_direction[0]
                    ]
                ),
            )
        else:  # moving vertical
            coords, path = map(
                list,
                zip(
                    *obstructions_map.get_column(current_position[0])[
                        (
                            current_position[1] + current_direction[1]
                        ) :: current_direction[1]
                    ]
                ),
            )

        try:
            distance_to_obstruction: int = path.index(MapField.OBSTRUCTION)
            return coords[:distance_to_obstruction], distance_to_obstruction

        except ValueError:
            # no obstruction in the path; guard leaves map
            return coords, None

    def rotate_guard(self, old_direction: tuple[int, int]) -> tuple[int, int]:
        match (old_direction):
            case (0, -1):
                return (1, 0)
            case (1, 0):
                return (0, 1)
            case (0, 1):
                return (-1, 0)
            case _:
                return (0, -1)

    def check_path_for_loops(
        self,
        visited_positions_with_directions: set[tuple[tuple[int, int], tuple[int, int]]],
        current_position: tuple[int, int],
        current_direction: tuple[int, int],
        new_obstruction_position: tuple[int, int],
    ) -> bool:

        new_map = self.map.copy()
        new_map[new_obstruction_position] = MapField.OBSTRUCTION

        temp_visited_positions_with_directions = (
            visited_positions_with_directions.copy()
        )

        guard_x, guard_y = current_position

        while True:
            _, distance_to_obstruction = self.get_path_and_distance_to_next_obstruction(
                new_map, (guard_x, guard_y), current_direction
            )

            if distance_to_obstruction == None:
                # no obstruction in the path; guard leaves map
                return False

            else:
                # move guard
                for position in [
                    (
                        guard_x + (current_direction[0] * i),
                        guard_y + (current_direction[1] * i),
                    )
                    for i in range(1, (distance_to_obstruction + 1))
                ]:
                    if (
                        position,
                        current_direction,
                    ) in temp_visited_positions_with_directions:
                        # loop found
                        return True

                    temp_visited_positions_with_directions.add(
                        (position, current_direction)
                    )

                guard_x += current_direction[0] * distance_to_obstruction
                guard_y += current_direction[1] * distance_to_obstruction

                # change direction
                current_direction = self.rotate_guard(current_direction)


class MapField(Enum):
    EMPTY = "."
    OBSTRUCTION = "#"
    GUARD_STARTING_POSITION = "^"
