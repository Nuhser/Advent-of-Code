from collections import defaultdict
from typing import override
from utility.sorting import merge_sort
import aoc_util as aoc


class Solution(aoc.AbstractSolution):
    @override
    def parse(self, puzzle_input: list[str]) -> None:
        self.hands: list['Solution.Hand'] = []

        for hand in aoc.parse_input(puzzle_input, " "):
            self.hands.append(self.Hand(hand))


    @override
    def part1(self) -> tuple[str, (int | float | str | None)]:
        self.card_order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

        hands: list['Solution.Hand'] = self.hands.copy()
        merge_sort(
            hands,
            self.compare_hands_without_joker
        )

        total_winnings: int = 0
        for idx, hand in enumerate(hands):
            total_winnings += (idx + 1) * hand.bid

        return f"Total winnings: {total_winnings}", total_winnings


    @override
    def part2(self) -> tuple[str, (int | float | str | None)]:
        self.card_order = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

        hands: list['Solution.Hand'] = self.hands.copy()
        merge_sort(
            hands,
            self.compare_hands_with_joker
        )

        total_winnings: int = 0
        for idx, hand in enumerate(hands):
            total_winnings += (idx + 1) * hand.bid

        return f"Total winnings: {total_winnings}", total_winnings
    

    def compare_hands_with_joker(self, hand1: 'Solution.Hand', hand2: 'Solution.Hand') -> bool:
        return self.compare_hands(hand1, hand2, True)
    

    def compare_hands_without_joker(self, hand1: 'Solution.Hand', hand2: 'Solution.Hand') -> bool:
        return self.compare_hands(hand1, hand2, False)


    def compare_hands(
        self,
        hand1: 'Solution.Hand',
        hand2: 'Solution.Hand',
        with_joker: bool
    ) -> bool:
        
        hand1_value: int = self.get_hand_value(hand1, with_joker)
        hand2_value: int = self.get_hand_value(hand2, with_joker)

        if hand1_value != hand2_value:
            return hand1_value < hand2_value
        
        for idx in range(5):
            card1_value: int = self.card_order.index(hand1.hand_string[idx])
            card2_value: int = self.card_order.index(hand2.hand_string[idx])

            if card1_value == card2_value:
                continue

            return card1_value < card2_value
        
        raise RuntimeError(f"ERROR: Hands '{hand1.hand_string}' and '{hand2.hand_string} are not comparable.")


    def get_hand_value(self, hand: 'Solution.Hand', with_joker: bool) -> int:
        """
        Value Order:

        - 5 of a kind
        - 4 of a kind
        - full house
        - 3 of a kind
        - 2 pairs
        - 1 pair
        - high card
        """

        unique_cards: int = len(hand.cards)
        joker_number: int = hand.cards.get("J") if hand.cards.get("J") != None else 0 # type: ignore

        match unique_cards:
            case 1:
                # 5 of a kind
                return 6

            case 2:
                if any(value == 4 for value in hand.cards.values()):
                    if with_joker and (joker_number > 0):
                        # 5 of a kind
                        return 6
                    else:
                        # 4 of a kind
                        return 5

                if with_joker and (joker_number > 0):
                    # 5 of a kind
                    return 6
                else:
                    # full house
                    return 4

            case 3:
                if any(value == 3 for value in hand.cards.values()):
                    if with_joker and (joker_number > 0):
                        # 4 of a kind
                        return 5
                    else:
                        # 3 of a kind
                        return 3

                if with_joker and (joker_number == 2):
                    # 4 of a kind
                    return 5
                elif with_joker and (joker_number == 1):
                    # full house
                    return 4
                else:
                    # 2 pairs
                    return 2

            case 4:
                if with_joker and (joker_number > 0):
                    # 3 of a kind
                    return 3
                else:
                    # 1 pair
                    return 1

            case _:
                if with_joker and (joker_number == 1):
                    # 1 pair
                    return 1
                else:
                    # high card
                    return 0

    class Hand:
        def __init__(self, hand_data: list[str]):
            self.hand_string: str = hand_data[0]
            self.bid: int = int(hand_data[1])
            self.cards: defaultdict[str, int] = defaultdict(lambda: int(0))

            for card in hand_data[0]:
                self.cards[card] += 1