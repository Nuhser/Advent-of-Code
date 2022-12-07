import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.turns = aoc.parse_input(puzzle_input, " ")

    def part1(self) -> tuple[str, (int | str)]:
        decryption = {
            "A": ("Z", "Y"),
            "B": ("X", "Z"),
            "C": ("Y", "X"),
            "X": 1,
            "Y": 2,
            "Z": 3
        }

        total_score = 0
        for elf, player in self.turns:
            win_multiplier = 2 if decryption[elf][1] == player else (0 if decryption[elf][0] == player else 1)
            total_score += (3 * win_multiplier) + decryption[player]

        return f"Your total score is {total_score}.", total_score

    def part2(self) -> tuple[str, (int | str)]:
        decryption = {
            "A": ("C", "B", 1),
            "B": ("A", "C", 2),
            "C": ("B", "A", 3)
        }

        total_score = 0
        for elf, player in self.turns:
            match player:
                case "X":
                    total_score += decryption[decryption[elf][0]][2]
                case "Y":
                    total_score += decryption[elf][2] + 3
                case "Z":
                    total_score += decryption[decryption[elf][1]][2] + 6

        return f"Your total score is {total_score}.", total_score