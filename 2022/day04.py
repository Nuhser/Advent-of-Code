import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.section_pairs = []
        for range1, range2 in aoc.parse_input(puzzle_input, ",", "-", cast_to=int):
            self.section_pairs.append((set(range(range1[0], range1[1] + 1)), set(range(range2[0], range2[1] + 1))))

    def part1(self) -> str:  
        doubled_sections = 0
        for section1, section2 in self.section_pairs:
            if section1.issubset(section2) or section2.issubset(section1):
                doubled_sections += 1

        return f"Total number of unnecessary sections: {doubled_sections}"

    def part2(self) -> str:
        intersections = 0
        for section1, section2 in self.section_pairs:
            if not section1.isdisjoint(section2):
                intersections += 1

        return f"Total number of unnecessary sections: {intersections}"