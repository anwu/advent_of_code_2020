import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    new_inputs = []

    for line in inputs:
        new_inputs.append(int(line))
    return new_inputs


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def check_encoding_rule(inputs, index):
    """Returns True if the number at index is the sum of 2 of the previous 25 numbers"""
    for i in range(1, 26):
        diff = inputs[index] - inputs[index - i]
        if diff in inputs[index-25:index]:
            return True

    return False


def find_bad_number(inputs):
    """Tests each input after the preamble if it passes the encoding rule"""
    for index in range(25, len(inputs)):
        result = check_encoding_rule(inputs, index)
        if not result:
            return index, inputs[index]


def find_encryption_weakness(inputs, fault_index):
    """Returns the sum of min/max numbers of the contiguous range sum of the fault number"""
    weakness_numbers = []

    for index in range(len(inputs)):
        if index == fault_index:
            weakness_numbers = []
            continue
        weakness_numbers.append(inputs[index])

        while sum(weakness_numbers) > inputs[fault_index]:
            weakness_numbers.pop(0)

        if sum(weakness_numbers) == inputs[fault_index] and len(weakness_numbers) > 2:
            return min(weakness_numbers) + max(weakness_numbers)


def main():
    """Main function"""
    args = parse_arguments()
    
    inputs = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    fault_index, bad_number = find_bad_number(inputs)
    print("[Part 1]\nBad Number: {}\n".format(bad_number))
    
    ####################
    #      Part 2      #
    ####################
    encryption_weakness = find_encryption_weakness(inputs, fault_index)
    print("[Part 2]\nEncryption Weakness: {}".format(encryption_weakness))
    

if __name__ == "__main__":
    main()