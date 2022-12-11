import aoc_util as aoc
import math

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.monkeys: list[Solution.Monkey] = []
        for block in aoc.parse_input_with_blocks(puzzle_input, ":"):
            self.monkeys.append(self.Monkey(
                start_items=[int(item.strip()) for item in block[1][1].split(",")],
                operation=block[2][1].strip().split()[2:],
                divider=int(block[3][1].strip().split()[2]),
                true_monkey=int(block[4][1].strip().split()[3]),
                false_monkey=int(block[5][1].strip().split()[3])
            ))

    def part1(self) -> tuple[str, (int | str | None)]:
        for _ in range(20):
            for idx, monkey in enumerate(self.monkeys):
                for item in monkey.items:
                    a = item if monkey.operation[0] == "old" else int(monkey.operation[0])
                    b = item if monkey.operation[2] == "old" else int(monkey.operation[2])

                    match monkey.operation[1]:
                        case "+":
                            item = a + b
                        # case "-":
                        #     item = a - b
                        case "*":
                            item = a * b
                        # case "/":
                            # item = a / b
                        case _:
                            raise RuntimeError(f"Unknown operator in monkey {idx}: '{monkey.operation[1]}'")

                    item //= 3
                    monkey.inspected_items += 1

                    if (item % monkey.divider) == 0:
                        self.monkeys[monkey.true_monkey].items.append(item)
                    else:
                        self.monkeys[monkey.false_monkey].items.append(item)

                monkey.items.clear()

        if self.verbose:
            for idx, monkey in enumerate(self.monkeys):
                print(f"Monkey {idx} inspected items {monkey.inspected_items} times.")

        solution = math.prod(sorted([monkey.inspected_items for monkey in self.monkeys])[-2:])
        return f"The level of monkey business is {solution}.", solution

    def part2(self) -> tuple[str, (int | str | None)]:
        mod_factor = math.prod([monkey.divider for monkey in self.monkeys])

        for _ in range(10000):
            for idx, monkey in enumerate(self.monkeys):
                for item in monkey.items:
                    a = item if monkey.operation[0] == "old" else int(monkey.operation[0])
                    b = item if monkey.operation[2] == "old" else int(monkey.operation[2])

                    match monkey.operation[1]:
                        case "+":
                            item = a + b
                        case "*":
                            item = a * b
                        case _:
                            raise RuntimeError(f"Unknown operator in monkey {idx}: '{monkey.operation[1]}'")

                    monkey.inspected_items += 1

                    item %= mod_factor

                    if (item % monkey.divider) == 0:
                        self.monkeys[monkey.true_monkey].items.append(item)
                    else:
                        self.monkeys[monkey.false_monkey].items.append(item)

                monkey.items.clear()

        if self.verbose:
            for idx, monkey in enumerate(self.monkeys):
                print(f"Monkey {idx} inspected items {monkey.inspected_items} times.")

        solution = math.prod(sorted([monkey.inspected_items for monkey in self.monkeys])[-2:])
        return f"The level of monkey business is {solution}.", solution

    class Monkey:
        def __init__(self, start_items: list[int], operation, divider: int, true_monkey: int, false_monkey: int) -> None:
            self.items = start_items
            self.operation = operation
            self.divider = divider
            self.true_monkey = true_monkey
            self.false_monkey = false_monkey
            self.inspected_items = 0