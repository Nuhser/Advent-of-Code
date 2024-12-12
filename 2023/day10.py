from typing import override

import aoc_util as aoc
from utility.mapping import Map, flood_fill_area
from utility.terminal_formatting import Color


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        # map all tiles and save start coordinates
        self.pipe_map = Map(aoc.parse_input(puzzle_input))
        self.start_coords = self.pipe_map.find_coords("S")

        # replace "S" with the correct pipe part
        neighbors = self.pipe_map.get_matching_neighbors(
            self.start_coords,
            self.is_pointing_to_current_pipe,
            diagonal=False,
        )
        diff1 = (
            neighbors[0][0][0] - self.start_coords[0],
            neighbors[0][0][1] - self.start_coords[1],
        )
        diff2 = (
            neighbors[1][0][0] - self.start_coords[0],
            neighbors[1][0][1] - self.start_coords[1],
        )

        match (diff1, diff2):
            case ((1, 0), (-1, 0)) | ((-1, 0), (1, 0)):
                self.pipe_map[self.start_coords] = "-"
            case ((0, 1), (0, -1)) | ((0, -1), (0, 1)):
                self.pipe_map[self.start_coords] = "|"
            case ((1, 0), (0, -1)) | ((0, -1), (1, 0)):
                self.pipe_map[self.start_coords] = "L"
            case ((-1, 0), (0, -1)) | ((0, -1), (-1, 0)):
                self.pipe_map[self.start_coords] = "J"
            case ((1, 0), (0, 1)) | ((0, 1), (1, 0)):
                self.pipe_map[self.start_coords] = "F"
            case ((-1, 0), (0, 1)) | ((0, 1), (-1, 0)):
                self.pipe_map[self.start_coords] = "7"

    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        main_loop_length: int = len(self.find_main_loop())

        return (
            f"Loop consists of {main_loop_length} pipes. Furthest distance to start a position {int(main_loop_length / 2)}.",
            int(main_loop_length / 2),
        )

    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        """
        Due to the iterativ flood fill algorithm, this part isn't very efficient. The calculation took ~140s.
        Unfortunately, the recursive flood fill algorithm needed to much recursion depth.
        """

        main_loop = self.find_main_loop()

        expanded_main_loop: list[tuple[int, int]] = []
        expanded_pipe_map = Map([])

        map_dimensions = self.pipe_map.get_dimensions()

        # expand map by doubling it in size
        for y in range(map_dimensions[1]):
            for x in range(map_dimensions[0]):
                expanded_pipe_map[x * 2, y * 2] = self.pipe_map[x, y]

                if (x, y) not in main_loop:
                    expanded_pipe_map[(x * 2) + 1, y * 2] = "."
                    expanded_pipe_map[x * 2, (y * 2) + 1] = "."
                    expanded_pipe_map[(x * 2) + 1, (y * 2) + 1] = "."

                else:
                    expanded_main_loop.append((x * 2, y * 2))

                    match self.pipe_map[x, y]:
                        case "-":
                            expanded_main_loop.append(((x * 2) + 1, y * 2))
                            expanded_pipe_map[(x * 2) + 1, y * 2] = "-"
                            expanded_pipe_map[x * 2, (y * 2) + 1] = "."
                        case "|":
                            expanded_main_loop.append((x * 2, (y * 2) + 1))
                            expanded_pipe_map[(x * 2) + 1, y * 2] = "."
                            expanded_pipe_map[x * 2, (y * 2) + 1] = "|"
                        case "L":
                            expanded_main_loop.append(((x * 2) + 1, y * 2))
                            expanded_pipe_map[(x * 2) + 1, y * 2] = "-"
                            expanded_pipe_map[x * 2, (y * 2) + 1] = "."
                        case "7":
                            expanded_main_loop.append((x * 2, (y * 2) + 1))
                            expanded_pipe_map[(x * 2) + 1, y * 2] = "."
                            expanded_pipe_map[x * 2, (y * 2) + 1] = "|"
                        case "F":
                            expanded_main_loop.append(((x * 2) + 1, y * 2))
                            expanded_main_loop.append((x * 2, (y * 2) + 1))
                            expanded_pipe_map[(x * 2) + 1, y * 2] = "-"
                            expanded_pipe_map[x * 2, (y * 2) + 1] = "|"
                        case _:
                            expanded_pipe_map[(x * 2) + 1, y * 2] = "."
                            expanded_pipe_map[x * 2, (y * 2) + 1] = "."

                    expanded_pipe_map[(x * 2) + 1, (y * 2) + 1] = "."

        max_x = map_dimensions[0] - 1
        max_y = map_dimensions[1] - 1

        # add ground as padding around the map
        for x in range(-1, (max_x * 2) + 2):
            expanded_pipe_map[x, -1] = "."
            expanded_pipe_map[x, (max_y * 2) + 1] = "."

        for y in range(-1, (max_y * 2) + 2):
            expanded_pipe_map[-1, y] = "."
            expanded_pipe_map[(max_x * 2) + 1, y] = "."

        print("Expanded map.")

        # flood fill outside area
        outside_area: list[tuple[int, int]] = flood_fill_area(
            expanded_pipe_map,
            (-1, -1),
            lambda _, neighbor: (neighbor[0] not in expanded_main_loop),
        )

        print(f"Number of flood filled tiles: {len(outside_area)}\n")

        # print expanded map
        if self.verbose:
            for y in range(-1, (max_y * 2) + 2):
                line: list[str] = []
                for x in range(-1, (max_x * 2) + 2):
                    if (x, y) in outside_area:
                        line.append(Color.RED + expanded_pipe_map[x, y] + Color.DEFAULT)
                    elif (x, y) in expanded_main_loop:
                        line.append(
                            Color.YELLOW + expanded_pipe_map[x, y] + Color.DEFAULT
                        )
                    else:
                        line.append(
                            Color.GREEN + expanded_pipe_map[x, y] + Color.DEFAULT
                        )

                print("".join(line))

        # count tiles inside the original loop
        inside_loop: list[tuple[int, int]] = []
        for y in range(0, (max_y * 2) + 1, 2):
            for x in range(0, (max_x * 2) + 1, 2):
                if ((x, y) not in expanded_main_loop) and ((x, y) not in outside_area):
                    inside_loop.append((x, y))

        return (
            f"There are {len(inside_loop)} tiles enclosed inside the main loop.",
            len(inside_loop),
        )

    def find_main_loop(self) -> list[tuple[int, int]]:
        # find starting direction
        current_pipe = self.pipe_map.get_matching_neighbors(
            self.start_coords, self.is_pointing_to_current_pipe, diagonal=False
        )[0]
        current_direction = (
            current_pipe[0][0] - self.start_coords[0],
            current_pipe[0][1] - self.start_coords[1],
        )
        main_loop: list[tuple[int, int]] = [self.start_coords, current_pipe[0]]

        while True:
            if self.verbose:
                print(
                    f"Looking at pipe #{len(main_loop)} '{current_pipe[1]}' (Direction: {current_direction})"
                )

            new_pipe: tuple[int, int]

            match current_pipe[1]:
                case "-" | "|":
                    new_pipe = (
                        current_pipe[0][0] + current_direction[0],
                        current_pipe[0][1] + current_direction[1],
                    )
                case "L":
                    if current_direction == (0, 1):
                        new_pipe = (current_pipe[0][0] + 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] - 1)
                case "F":
                    if current_direction == (0, -1):
                        new_pipe = (current_pipe[0][0] + 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] + 1)
                case "J":
                    if current_direction == (0, 1):
                        new_pipe = (current_pipe[0][0] - 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] - 1)
                case "7":
                    if current_direction == (0, -1):
                        new_pipe = (current_pipe[0][0] - 1, current_pipe[0][1])
                    else:
                        new_pipe = (current_pipe[0][0], current_pipe[0][1] + 1)
                case _:
                    raise ValueError(
                        f"ERROR: Unexpected pipe type '{current_pipe[1]}'! You may have lost the main loop."
                    )

            current_direction = (
                new_pipe[0] - current_pipe[0][0],
                new_pipe[1] - current_pipe[0][1],
            )
            current_pipe = (new_pipe, self.pipe_map[new_pipe])

            if current_pipe[0] == self.start_coords:
                break

            main_loop.append(new_pipe)

        return main_loop

    def is_pointing_to_current_pipe(
        self, current_coords: tuple[int, int], other_pipe: tuple[tuple[int, int], str]
    ) -> bool:
        if current_coords[0] > other_pipe[0][0]:
            return other_pipe[1] in ["-", "L", "F"]

        elif current_coords[0] < other_pipe[0][0]:
            return other_pipe[1] in ["-", "J", "7"]

        elif current_coords[1] > other_pipe[0][1]:
            return other_pipe[1] in ["|", "F", "7"]

        elif current_coords[1] < other_pipe[0][1]:
            return other_pipe[1] in ["|", "L", "J"]

        else:
            raise ValueError(
                f"ERROR: No neighboring pipes are pointing into current pipe at X={current_coords[0]} & Y={current_coords[1]}."
            )
