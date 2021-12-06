from numpy import sign 


if __name__ == '__main__':
    vent_lines = []
    vent_map = dict()

    # read input file
    with open('./input.txt') as input_file:
        for line in [line.strip() for line in input_file.readlines()]:
            vent_lines.append([int(n) for pair in line.split(' -> ') for n in pair.split(',')])

    # remove non horizontal or verticel lines
    vent_lines = [line for line in vent_lines if line[0] == line[2] or line[1] == line[3]]

    # fill map
    for line in vent_lines:
        # vertical line
        if (line[0] == line[2]):
            direction = sign(line[3] - line[1])
            for y in range(line[1], line[3] + direction, direction):
                if (line[0], y) not in vent_map:
                    vent_map[(line[0], y)] = 1
                else:
                    vent_map[(line[0], y)] += 1

        # horizontal line
        elif (line[1] == line[3]):
            direction = sign(line[2] - line[0])
            for x in range(line[0], line[2] + direction, direction):
                if (x, line[1]) not in vent_map:
                    vent_map[(x, line[1])] = 1
                else:
                    vent_map[(x, line[1])] += 1

        # Shouldn't hapen in this part of the challenge.
        else:
            print("ERROR: Line not horizontal or vertical")

    # count dangerous coords
    count = len([coord for coord in vent_map if vent_map[coord] > 1])

    print(f'Solution: {count}')