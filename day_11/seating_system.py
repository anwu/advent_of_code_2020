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


def get_adjacents(seat_map, row, col):
    """Get the adjacent seats around the current seat"""
    adjacents = []

    if row - 1 >= 0:
        adjacents.append(seat_map[row-1][col]) # add top
        if col - 1 >= 0:
            adjacents.append(seat_map[row-1][col-1]) # add top left
        if col + 1 < len(seat_map[row]):
            adjacents.append(seat_map[row-1][col+1]) # add top right
    if row + 1 < len(seat_map):
        adjacents.append(seat_map[row+1][col]) # add bot
        if col - 1 >= 0:
            adjacents.append(seat_map[row+1][col-1]) # add bot left
        if col + 1 < len(seat_map[row]):
            adjacents.append(seat_map[row+1][col+1]) # add bot right
    if col - 1 >= 0:
        adjacents.append(seat_map[row][col-1]) # add left
    if col + 1 < len(seat_map[row]):
        adjacents.append(seat_map[row][col+1]) # add right

    return adjacents


def get_visibles(seat_map, row, col):
    """Get the first seat in each direction from the current seat"""
    visibles = []

    for i in range(row-1, -1, -1): # add first top not floor
        if seat_map[i][col] != '.':
            visibles.append(seat_map[i][col])
            break
    
    i = row - 1
    j = col - 1
    while i >= 0 and j >= 0 : # add first top left not floor
        if seat_map[i][j] != '.':
            visibles.append(seat_map[i][j])
            break
        i -= 1
        j -= 1

    i = row - 1
    j = col + 1
    while i >= 0 and j < len(seat_map[0]): # add first top right not floor
        if seat_map[i][j] != '.':
            visibles.append(seat_map[i][j])
            break
        i -= 1
        j += 1

    for i in range(row+1, len(seat_map)): # add first bot not floor
        if seat_map[i][col] != '.':
            visibles.append(seat_map[i][col])
            break
    
    i = row + 1
    j = col - 1
    while i < len(seat_map) and j >= 0 : # add first bot left not floor
        if seat_map[i][j] != '.':
            visibles.append(seat_map[i][j])
            break
        i += 1
        j -= 1

    i = row + 1
    j = col + 1
    while i < len(seat_map) and j < len(seat_map[0]): # add first bot right not floor
        if seat_map[i][j] != '.':
            visibles.append(seat_map[i][j])
            break
        i += 1
        j += 1

    for i in range(col-1, -1, -1): # add first left not floor
        if seat_map[row][i] != '.':
            visibles.append(seat_map[row][i])
            break

    for i in range(col+1, len(seat_map[0])): # add first right not floor
        if seat_map[row][i] != '.':
            visibles.append(seat_map[row][i])
            break

    return visibles
    

def p1_activate_seat_rule(seat_map):
    """Applies an iteration of the rules for part 1"""
    seat_map_copy = copy.deepcopy(seat_map)
    seat_change = False

    for row in range(len(seat_map)):
        for col in range(len(seat_map[row])):
            adjacents = get_adjacents(seat_map_copy, row, col)
            if seat_map_copy[row][col] == 'L' and adjacents.count('#') == 0:
                seat_map[row][col] = '#'
                seat_change = True
            elif seat_map_copy[row][col] == '#' and adjacents.count('#') >= 4:
                seat_map[row][col] = 'L'
                seat_change = True

    return seat_change


def p2_activate_seat_rule(seat_map):
    """Applies an iteration of the rules for part 2"""
    seat_map_copy = copy.deepcopy(seat_map)
    seat_change = False

    for row in range(len(seat_map)):
        for col in range(len(seat_map[row])):
            visible_seats = get_visibles(seat_map_copy, row, col)
            if seat_map_copy[row][col] == 'L' and visible_seats.count('#') == 0:
                seat_map[row][col] = '#'
                seat_change = True
            elif seat_map_copy[row][col] == '#' and visible_seats.count('#') >= 5:
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
            seat_change = p1_activate_seat_rule(seat_map_copy)
        elif part == 2:
            seat_change = p2_activate_seat_rule(seat_map_copy)

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