import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    instructions = []

    for line in inputs:
        instructions.append((line[0], int(line[1:])))

    return instructions


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def move_direction(coordinates, direction, value):
    """Move the ship towards the direction by value"""
    if direction == 0 or direction == 'N': # move north
        coordinates[0] += value
    elif direction == 180 or direction == 'S': # move south
        coordinates[0] -= value
    elif direction == 90 or direction == 'E': # move east
        coordinates[1] += value
    elif direction == 270 or direction == 'W': # move west
        coordinates[1] -= value


def rotate_direction(curr_direction, new_direction, degrees):
    """Rotate the direction the ship is facing"""
    if new_direction == 'L':
        return (curr_direction + 360 - degrees) % 360
    elif new_direction == 'R':
        return (curr_direction + degrees) % 360


def rotate_waypoint(waypoint, new_direction, degrees):
    """Rotates the both axis of the waypoint"""
    if new_direction == 'L':
        clockwise_rotation = 360 - degrees
    else:
        clockwise_rotation = degrees
    temp_x, temp_y = waypoint

    if clockwise_rotation == 90:
        waypoint[0] = -1 * temp_y
        waypoint[1] = temp_x
    elif clockwise_rotation == 180:
        waypoint[0] = -1 * temp_x
        waypoint[1] = -1 * temp_y
    elif clockwise_rotation == 270:
        waypoint[0] = temp_y
        waypoint[1] = -1 * temp_x


def p1_get_manhattan_distance(instructions):
    """Gets the manhattan distance of the coordinates by executing instructions"""
    coordinates = [0, 0]
    direction = 90

    for instruction in instructions:
        if instruction[0] == 'F':
            move_direction(coordinates, direction, instruction[1])
        elif instruction[0] == 'L' or instruction[0] == 'R':
            direction = rotate_direction(direction, instruction[0], instruction[1])
        else:
            move_direction(coordinates, instruction[0], instruction[1])

    return sum(abs(coord) for coord in coordinates)


def p2_get_manhattan_distance(instructions):
    """Gets the manhattan distance of the coordinates using waypoints"""
    coordinates = [0, 0]
    waypoint = [1, 10]

    for instruction in instructions:
        if instruction[0] == 'F':
            coordinates[0] += waypoint[0] * instruction[1]
            coordinates[1] += waypoint[1] * instruction[1]
        elif instruction[0] == 'L' or instruction[0] == 'R':
            rotate_waypoint(waypoint, instruction[0], instruction[1])
        else:
            move_direction(waypoint, instruction[0], instruction[1])

    return sum(abs(coord) for coord in coordinates)


def main():
    """Main function"""
    args = parse_arguments()
    
    instructions = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    manhattan_distance = p1_get_manhattan_distance(instructions)
    print("[Part 1]\nManhattan Distance: {}\n".format(manhattan_distance))
    
    ####################
    #      Part 2      #
    ####################
    manhattan_distance = p2_get_manhattan_distance(instructions)
    print("[Part 2]\nManhattan Distance: {}".format(manhattan_distance))

if __name__ == "__main__":
    main()