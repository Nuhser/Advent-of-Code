import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.signal = puzzle_input[0]

    def part1(self) -> str:
        packet_start_marker = [""] * 4
        for idx, char in enumerate(self.signal):
            packet_start_marker[0] = packet_start_marker[1]
            packet_start_marker[1] = packet_start_marker[2]
            packet_start_marker[2] = packet_start_marker[3]
            packet_start_marker[3] = char

            if ((len(set(packet_start_marker)) == 4) and (not "" in packet_start_marker)):
                return f"First start-of-packet marker '{''.join(packet_start_marker)}' after {idx + 1} characters"

        return "Error: No start-of-packet marker found"

    def part2(self) -> str:
        message_start_marker = [""] * 14
        for idx, char in enumerate(self.signal):
            message_start_marker = [message_start_marker[i] for i in range(1, len(message_start_marker))] + [char]

            if ((len(set(message_start_marker)) == 14) and (not "" in message_start_marker)):
                return f"First start-of-message marker '{''.join(message_start_marker)}' after {idx + 1} characters"

        return "Error: No start-of-message marker found"
