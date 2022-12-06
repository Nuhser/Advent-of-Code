import aoc_util as aoc
import itertools

class Solution(aoc.AbstractSolution):
    def parse(self, puzzle_input: list[str]) -> None:
        self.draws = aoc.parse_input(puzzle_input[0:1], ",", cast_to=int)[0]
        self.cards = aoc.parse_input_with_blocks(puzzle_input[2:], "", cast_to=int)
        self.cards = [[list(itertools.chain.from_iterable(card)), [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]] for card in self.cards]

    def part1(self) -> str:
        # mark cards & find solution
        solution_found = False
        for number in self.draws:
            for card in self.cards:
                if card[0].count(number) > 0:
                    idx = card[0].index(number)
                    card[0][idx] = '#'
                    card[1][idx % 5] += 1
                    card[2][int(idx / 5)] += 1

                    if card[1].count(5) > 0 or card[2].count(5) > 0:
                        solution_found = True
                        unmarked_sum = sum([n for n in card[0] if n != '#'])

                        return f'BINGO!!!\n--------\n\nCard:\t{card[0][0 : 5]}\n\t{card[0][5 : 10]}\n\t{card[0][10 : 15]}\n\t{card[0][15 : 20]}\n\t{card[0][20 : 25]}\n\nSum of Unmarked Numbers: {unmarked_sum}\nLast Number: {number}\n\nSolution: {unmarked_sum * number}'
                    
                if solution_found:
                    break

            if solution_found:
                break

        return "Error: No BINGO found!"

    def part2(self) -> str:
        # mark cards & find solution
        solution_found = False
        for number in self.draws:
            for idx, card in enumerate(self.cards):
                if card[0].count(number) > 0:
                    idx = card[0].index(number)
                    card[0][idx] = '#'
                    card[1][idx % 5] += 1
                    card[2][int(idx / 5)] += 1

                    if card[1].count(5) > 0 or card[2].count(5) > 0:
                        card.append('#')

                        if len(self.cards) == 1:
                            solution_found = True

            if not solution_found:
                self.cards = [card for card in self.cards if len(card) < 4]
            else:
                break

        card = self.cards[0]
        unmarked_sum = sum([n for n in card[0] if n != '#'])

        return f'BINGO!!!\n--------\n\nCard:\t{card[0][0 : 5]}\n\t{card[0][5 : 10]}\n\t{card[0][10 : 15]}\n\t{card[0][15 : 20]}\n\t{card[0][20 : 25]}\n\nSum of Unmarked Numbers: {unmarked_sum}\nLast Number: {number}\n\nSolution: {unmarked_sum * number}'
