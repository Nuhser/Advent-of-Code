if __name__ == '__main__':
    # read input
    with open('input.txt') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
        input_file.close()

    oxygen = lines
    for i in range(len(oxygen[0])):
        digit_counts = [0, 0]
        for value in oxygen:
            digit_counts[int(value[i])] += 1

        oxygen = [value for value in oxygen if (value[i] == '0')] \
            if digit_counts[0] > digit_counts[1] \
            else [value for value in oxygen if (value[i] == '1')]

        if len(oxygen) <= 1:
            break

    co2 = lines
    for i in range(len(co2[0])):
        digit_counts = [0, 0]
        for value in co2:
            digit_counts[int(value[i])] += 1

        co2 = [value for value in co2 if (value[i] == '0')] \
            if digit_counts[0] <= digit_counts[1] \
            else [value for value in co2 if (value[i] == '1')]

        if len(co2) <= 1:
            break

    print(f'Oxygen:\t{oxygen[0]} -> {int(oxygen[0], 2)}\nCO2:\t{co2[0]} -> {int(co2[0], 2)}\n\nLife Support Rating: {int(oxygen[0], 2) * int(co2[0], 2)}')