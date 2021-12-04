from os import system
import os
import sys


if __name__ == '__main__':
    with open('./input.txt') as input_file:
        # get drawn numbers
        draws = [int(i) for i in input_file.readline().strip().split(',')]

        cards = []
        for line in [line.strip() for line in input_file.readlines()]:
            # create new BINGO-card
            if line == '':
                cards.append([[], [0,0,0,0,0], [0,0,0,0,0]])

            # fill card
            else:
                numbers = [int(number) for number in line.split(' ') if number.strip() != '']
                cards[-1][0] += numbers

        input_file.close()

    # mark cards
    for number in draws:
        for card in cards:
            if card[0].count(number) > 0:
                idx = card[0].index(number)
                card[0][idx] = '#'
                card[1][idx % 5] += 1
                card[2][int(idx / 5)] += 1

                if card[1].count(5) > 0 or card[2].count(5) > 0:
                    unmarked_sum = sum([n for n in card[0] if n != '#'])

                    print(f'BINGO!!!\n--------\n\nCard:\t{card[0][0 : 5]}\n\t{card[0][5 : 10]}\n\t{card[0][10 : 15]}\n\t{card[0][15 : 20]}\n\t{card[0][20 : 25]}\n')
                    print(f'Sum of Unmarked Numbers: {unmarked_sum}\nLast Number: {number}\n')
                    print(f'Solution: {unmarked_sum * number}')

                    sys.exit()
