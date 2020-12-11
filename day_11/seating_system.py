import argparse
import copy

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    seat_map = [[] for i in range(len(inputs))]

    for index, line in enumerate(inputs):
        seat_map[index] = list(line)
    
    return seat_map


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def _within_bounds(row_min, row_max, col_min, col_max, row, col):
    if row >= row_min and row < row_max and col >= col_min and col < col_max:
        return True
    return False 


def get_neighbors(seat_map, row, col, single_depth=False):
    """Get the neighboring seat in each direction from the current seat"""
    neighbors = []
    direction_ops = {'top_left': (-1, -1), 'top': (-1, 0), 'top_right': (-1, 1),
                     'bot_left': (1, -1), 'bot': (1, 0), 'bot_right': (1, 1),
                     'left': (0, -1), 'right': (0, 1)}

    row_min = col_min = 0
    row_max = len(seat_map)
    col_max = len(seat_map[0])

    for _, ops in direction_ops.items():
        i = row + ops[0]
        j = col + ops[1]
        while _within_bounds(row_min, row_max, col_min, col_max, i, j):
            if seat_map[i][j] != '.':
                neighbors.append(seat_map[i][j])
                break
            i += ops[0]
            j += ops[1]
            if single_depth:
                break

    return neighbors
    

def activate_seat_rule(seat_map, part=1):
    """Applies an iteration of the rules"""
    seat_map_copy = copy.deepcopy(seat_map)
    seat_change = False
    crowd_limit = 4 if part == 1 else 5
    single_depth = True if part == 1 else False

    for row in range(len(seat_map)):
        for col in range(len(seat_map[row])):
            neighbor_seats = get_neighbors(seat_map_copy, row, col, single_depth=single_depth)
            if seat_map_copy[row][col] == 'L' and neighbor_seats.count('#') == 0:
                seat_map[row][col] = '#'
                seat_change = True
            elif seat_map_copy[row][col] == '#' and neighbor_seats.count('#') >= crowd_limit:
                seat_map[row][col] = 'L'
                seat_change = True

    return seat_change


def count_occupied_seats(seat_map):
    """Returns the number of occupied seats in the map"""
    num_occupied = 0

    for row in range(len(seat_map)):
        num_occupied += seat_map[row].count('#')

    return num_occupied


def get_final_num_occupied_seats(seat_map, part=1):
    """Returns the final number of occupied seats after people calm the F down"""
    seat_map_copy = copy.deepcopy(seat_map)
    seat_change = True

    i = 1
    while seat_change:
        if part == 1:
            seat_change = activate_seat_rule(seat_map_copy, part=part)
        elif part == 2:
            seat_change = activate_seat_rule(seat_map_copy, part=part)
        i += 1

    num_occupied = count_occupied_seats(seat_map_copy)
    
    return num_occupied


def main():
    """Main function"""
    args = parse_arguments()
    
    seat_map = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    num_occupied_seats = get_final_num_occupied_seats(seat_map, part=1)
    print("[Part 1]\nNumber of Occupied Seats: {}\n".format(num_occupied_seats))

    ####################
    #      Part 2      #
    ####################
    num_occupied_seats = get_final_num_occupied_seats(seat_map, part=2)
    print("[Part 2]\nNumber of Occupied Seats: {}".format(num_occupied_seats))


if __name__ == "__main__":
    main()