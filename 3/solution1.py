if __name__ == '__main__':
    # read input
    with open('input.txt') as input_file:
        lines = input_file.readlines()
        input_file.close()

    # count 1s per digit
    counts = [int(d) for d in lines[0].strip()]
    for line in lines[1 :]:
        for i in range(len(counts)):
            counts[i] += int(line[i])

    gamma = ''
    epsilon = ''
    for count in counts:
        # get most common digit
        most_common_digit = int(count / (len(lines) / 2))

        # calculate gamma and epsilon
        gamma += str(most_common_digit)
        epsilon += str(0 if most_common_digit == 1 else 1)

    print(f'Gamma: {gamma} -> {int(gamma, 2)}\nEpsilon: {epsilon} -> {int(epsilon, 2)}\n\nPower Consumption: {int(gamma, 2) * int(epsilon, 2)}')

