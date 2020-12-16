from collections import deque
import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    return [int(x) for x in inputs[0].split(',')]


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def update_number_memory(number_memory, num, index):
    """Helper function to update the memory of the last 2 occurrences of a number"""
    num = str(num)
    if num not in number_memory:
        number_memory[num] = deque([index])
    else:
        number_memory[num].appendleft(index)
        if len(number_memory[num]) > 2:
            number_memory[num].pop()


def find_nth_number(starting_numbers, nth_iteration):
    """Finds the nth number of the sequence"""
    number_memory = {}
    number_sequence = starting_numbers

    # not a very good runtime...
    for index, num in enumerate(starting_numbers):
        update_number_memory(number_memory, num, index)
    prev_num = str(number_sequence[-1])
    for i in range(len(starting_numbers), nth_iteration):
        if prev_num in number_memory and len(number_memory[prev_num]) == 2:
            new_num = number_memory[prev_num][0] - number_memory[prev_num][1]
            number_sequence.append(new_num)
            update_number_memory(number_memory, new_num, i)
            prev_num = str(new_num)
        else:
            number_sequence.append(0)
            update_number_memory(number_memory, 0, i)
            prev_num = str(0)

    return number_sequence[-1]


def main():
    """Main function"""
    args = parse_arguments()
    
    starting_numbers = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    nth_number = find_nth_number(starting_numbers, 2020)
    print("[Part 1]\n2020th Number: {}\n".format(nth_number))

    ####################
    #      Part 2      #
    ####################
    nth_number = find_nth_number(starting_numbers, 30000000)
    print("[Part 1]\n30000000th Number: {}\n".format(nth_number))


if __name__ == "__main__":
    main()