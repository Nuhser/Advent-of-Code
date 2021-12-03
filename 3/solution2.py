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

        # print(digit_counts)

        new_oxygen = []
        for value in oxygen:
            if digit_counts[0] > digit_counts[1]:
                if value[i] == '0':
                    new_oxygen.append(value)
            else:
                if value[i] == '1':
                    new_oxygen.append(value)

        oxygen = new_oxygen

        if len(oxygen) <= 1:
            break

    co2 = lines
    for i in range(len(co2[0])):
        digit_counts = [0, 0]
        for value in co2:
            digit_counts[int(value[i])] += 1

        # print(digit_counts)

        new_co2 = []
        for value in co2:
            if digit_counts[0] <= digit_counts[1]:
                if value[i] == '0':
                    new_co2.append(value)
            else:
                if value[i] == '1':
                    new_co2.append(value)

        co2 = new_co2

        if len(co2) <= 1:
            break

    print(f'Oxygen: {oxygen[0]} -> {int(oxygen[0], 2)}\nCO2: {co2[0]} -> {int(co2[0], 2)}\n\nLife Support Rating: {int(oxygen[0], 2) * int(co2[0], 2)}')