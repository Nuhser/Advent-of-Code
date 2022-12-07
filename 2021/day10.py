import aoc_util as aoc

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.navigation_system = aoc.parse_input(puzzle_input)

    def part1(self) -> tuple[str, (int | str)]:
        syntax_error_score = 0
        for line in self.navigation_system:
            stack = [-1]
            for char in line:
                match char:
                    case ')':
                        if stack.pop() != '(':
                            syntax_error_score += 3
                            break
                    case ']':
                        if stack.pop() != '[':
                            syntax_error_score += 57
                            break
                    case '}':
                        if stack.pop() != '{':
                            syntax_error_score += 1197
                            break
                    case '>':
                        if stack.pop() != '<':
                            syntax_error_score += 25137
                            break
                    case _:
                        stack.append(char)

        return f'Syntax Error Score: {syntax_error_score}', syntax_error_score

    def part2(self) -> tuple[str, (int | str)]:
        scores = []
        for line in [line for line in self.navigation_system if not self.is_line_corrupted(line)]:
            stack = []
            for char in line:
                if char in [')', ']', '}', '>']:
                    stack.pop()
                else:
                    stack.append(char)

            score = 0
            for char in reversed(stack):
                score *= 5
                score += ['(', '[', '{', '<'].index(char) + 1

            scores.append(score)

        if self.verbose:
            print(f"Scores: {scores}\n")

        solution = sorted(scores)[len(scores) // 2]
        return f'Middle Score: {solution}', solution

    def is_line_corrupted(self, line: str) -> bool:
        stack = [-1]
        for char in line:
            match char:
                case ')':
                    if stack.pop() != '(':
                        return True
                case ']':
                    if stack.pop() != '[':
                        return True
                case '}':
                    if stack.pop() != '{':
                        return True
                case '>':
                    if stack.pop() != '<':
                        return True
                case _:
                    stack.append(char)

        return False