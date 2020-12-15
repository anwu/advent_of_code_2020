import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    start_time = int(inputs[0])
    bus_lines = inputs[1].split(',')

    return start_time, bus_lines


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def find_soonest_bus(start_time, bus_lines):
    """Find the soonest bus by looking at modulo remainder"""
    next_board_times = []

    bus_lines = list(filter(('x').__ne__, bus_lines))
    bus_lines = [int(x) for x in bus_lines]
    
    for line in bus_lines:
        next_board_times.append(line - (start_time % line))

    return min(next_board_times) * bus_lines[next_board_times.index(min(next_board_times))]


def find_soonest_aligned_departs(bus_lines):
    """Use the Chinese Remainder Theorem to find the aligned bus departures"""
    # https://www.youtube.com/watch?v=ru7mWZJlRQg&ab_channel=RandellHeyman
    bus_lines = [(index % int(line), int(line)) for index, line in enumerate(bus_lines) if line != 'x']

    _, inc = bus_lines[0]
    timestamp = inc

    for index, line in bus_lines[1:]:
        inc_count = 1

        while (timestamp + inc * inc_count) % line != line - index:
            inc_count += 1

        timestamp += inc * inc_count
        inc *= line

    return timestamp


def main():
    """Main function"""
    args = parse_arguments()
    
    start_time, bus_lines = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    soonest_bus_product = find_soonest_bus(start_time, bus_lines)
    print("[Part 1]\nID of Earliest Bus x Wait Time: {}\n".format(soonest_bus_product))

    ####################
    #      Part 2      #
    ####################
    aligned_depart_time = find_soonest_aligned_departs(bus_lines)
    print("[Part 2]\nSoonest Timestamp of Aligned Departs: {}".format(aligned_depart_time))


if __name__ == "__main__":
    main()