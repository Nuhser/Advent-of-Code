import aoc_util as aoc
import utility.util

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        # parse puzzle input
        start_positions, self.moves = aoc.parse_input_with_blocks(puzzle_input, block_delimiter="\n", strip_lines=False)

        # format moves
        self.moves = [move.split(" ") for move in self.moves]
        self.moves = [(int(move[1]), int(move[3]), int(move[5])) for move in self.moves]

        # format start position
        start_positions = [utility.util.split_string_in_chunks(row, 3, 1) for row in start_positions[: -1]]

        # initialize stacks
        self.initial_crates = [[] for _ in range(len(start_positions[0]))]
        for row in reversed(start_positions):
            for idx, crate in enumerate([crate.strip() for crate in row]):
                if crate != "":
                    self.initial_crates[idx].append(crate)

    def part1(self) -> tuple[str, (int | str)]:
        # do moves
        crates = [inner_list[:] for inner_list in self.initial_crates]
        for move in self.moves:
            for _ in range(move[0]):
                crates[move[2]-1].append(crates[move[1]-1].pop())

        solution = ''.join([crate[-1].replace('[', '').replace(']', '') for crate in crates])
        return f"Final top crates: {solution}", solution


    def part2(self) -> tuple[str, (int | str)]:
        # do moves
        crates = [inner_list[:] for inner_list in self.initial_crates]
        for move in self.moves:
            crates[move[2]-1]+= crates[move[1]-1][-move[0] :]
            crates[move[1]-1] = crates[move[1]-1][: -move[0]]

        solution = ''.join([crate[-1].replace('[', '').replace(']', '') for crate in crates])
        return f"Final top crates: {solution}", solution