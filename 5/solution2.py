from numpy import sign 


if __name__ == '__main__':
    vent_lines = []
    vent_map = dict()

    # read input file
    with open('./input.txt') as input_file:
        for line in [line.strip() for line in input_file.readlines()]:
            vent_lines.append([int(n) for pair in line.split(' -> ') for n in pair.split(',')])

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

        # diagonal lines
        else:
            x1, y1 = (line[0], line[1]) if line[0] < line[2] else (line[2], line[3])
            x2, y2 = (line[0], line[1]) if line[0] > line[2] else (line[2], line[3])
            gradient = (line[3] - line[1]) / (line[2] - line[0])
            b = y1 - int(x1 * gradient)

            while True:
                if (x1, y1) not in vent_map:
                    vent_map[(x1, y1)] = 1
                else:
                    vent_map[(x1, y1)] += 1

                x1 += 1
                y1 = int(x1 * gradient) + b

                if x1 == x2 and y1 == y2:
                    if (x1, y1) not in vent_map:
                        vent_map[(x1, y1)] = 1
                    else:
                        vent_map[(x1, y1)] += 1
                        
                    break

    # count dangerous coords
    count = len([coord for coord in vent_map if vent_map[coord] > 1])

    print(f'Solution: {count}')