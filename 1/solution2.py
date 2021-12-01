if __name__ == '__main__':
    with open('./input.txt') as input_file:
        depths = [int(line.strip()) for line in input_file.readlines()]
        input_file.close()

    sliding_sums = [sum(depths[i : i+3]) for i in range(len(depths[: -2]))]

    n_increases = 0
    last_depth = sliding_sums[0]
    for depth in sliding_sums[1 :]:
        if last_depth < depth:
            n_increases += 1
        last_depth = depth

    print(f'Total depth increasses: {n_increases}')