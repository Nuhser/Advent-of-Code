if __name__ == '__main__':
    with open('./input1.txt') as input_file:
        depths = []

        for line in input_file.readlines():
            depths.append(int(line.strip()))

        input_file.close()

    n_increases = 0
    last_depth = depths[0]
    for depth in depths[1 :]:
        if last_depth < depth:
            n_increases += 1
        last_depth = depth

    print(f'Total depth increasses: {n_increases}')