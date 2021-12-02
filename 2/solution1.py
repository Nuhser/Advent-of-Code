if __name__ == '__main__':
    commands = []

    with open('input.txt') as input_file:
        for line in input_file.readlines():
            line = line.strip().split(' ')
            commands.append((line[0], int(line[1])))

        input_file.close()

    horizontal = 0
    depth = 0

    for command in commands:
        if command[0] == 'forward':
            horizontal += command[1]
        elif command[0] == 'up':
            depth -= command[1]
        elif command[0] == 'down':
            depth += command[1]
        else:
            print(f'ERROR: Unknown command "{command[0]}"')

    print(f'Horizontal Position: {horizontal}\nDepth: {depth}\n\nSolution: {horizontal * depth}')