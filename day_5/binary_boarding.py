import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    seats = []

    for line in inputs:
        row = line[:7].replace('F', '0').replace('B', '1')
        col = line[-3:].replace('L', '0').replace('R', '1')
        row = int(row, 2)
        col = int(col, 2)
        seats.append((row, col))

    return seats


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def calculate_seat_id(seat):
    """Returns the seat id of the row and column of the seat"""
    return seat[0] * 8 + seat[1]


def get_max_seat_id(seats):
    """Gets the max seat id of all the seats"""
    max_id = 0
    for seat in seats:
        seat_id = calculate_seat_id(seat)
        max_id = seat_id if seat_id > max_id else max_id
    return max_id


def find_seat(seats):
    """Finds an empty seat between two seats between the first and last rows"""
    seat_ids = []

    for seat in seats:
        if seat[0] == 0 or seat[0] == 127:
            continue
        seat_ids.append(calculate_seat_id(seat))
    
    seat_ids.sort()

    for i in range(len(seat_ids)-2):
        if seat_ids[i] == seat_ids[i+1] - 2:
            return seat_ids[i] + 1


def main():
    """Main function"""
    args = parse_arguments()
    
    seats = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    max_seat_id = get_max_seat_id(seats)
    print("[Part 1]\nHighest Seat ID: {}\n".format(max_seat_id))

    ####################
    #      Part 2      #
    ####################
    seat_id = find_seat(seats)
    print("[Part 2]\nSeat ID: {}".format(seat_id))


if __name__ == "__main__":
    main()