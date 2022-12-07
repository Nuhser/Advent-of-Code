import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        connections = aoc.parse_input(puzzle_input, "-")

        self.cave_map = dict()
        for connection in connections:
            for cave in connection:
                if cave not in self.cave_map:
                    self.cave_map[cave] = [c for c in connection if c != cave]
                else:
                    self.cave_map[cave] += [c for c in connection if c != cave]

        if self.verbose:
            print(f"Cave Map: {self.cave_map}\n")

    def part1(self) -> tuple[str, (int | str)]:
        all_paths = [path for path in self.find_path_part1('start') if path[-1] == 'end']
        return f'Possible Paths: {len(all_paths)}', len(all_paths)

    def part2(self) -> tuple[str, (int | str)]:
        all_paths = [path for path in self.find_path_part2('start') if path[-1] == 'end']
        return f'Possible Paths: {len(all_paths)}', len(all_paths)

    def find_path_part1(self, cave: str, current_path: list[str]=[]) -> list[list[str]]:
        current_path.append(cave)

        if (cave == 'end'):
            return [current_path]

        next_paths = []
        for next_cave in filter(lambda c: c.isupper() or (c not in current_path), self.cave_map[cave]):
            next_paths += self.find_path_part1(next_cave, current_path.copy())
        
        return next_paths if (len(next_paths) > 0) else [current_path]

    def find_path_part2(self, cave: str, current_path: list[str]=[]) -> list[list[str]]:
        current_path.append(cave)

        if (cave == 'end'):
            return [current_path]

        next_paths = []
        small_room_double = not all((current_path.count(c) < 2) for c in current_path if c.islower())
        if small_room_double:
            for next_cave in filter(lambda c: c.isupper() or (c not in current_path), self.cave_map[cave]):
                next_paths += self.find_path_part2(next_cave, current_path.copy())
        else:
            for next_cave in filter(lambda c: c != 'start', self.cave_map[cave]):
                next_paths += self.find_path_part2(next_cave, current_path.copy())
        
        return next_paths if (len(next_paths) > 0) else [current_path]