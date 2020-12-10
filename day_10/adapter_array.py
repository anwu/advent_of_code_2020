import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    new_inputs = [int(line) for line in inputs]
    new_inputs.sort()
    new_inputs.insert(0, 0)
    new_inputs.insert(len(new_inputs), new_inputs[-1]+3)

    return new_inputs


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def get_jolt_diff_product(inputs):
    """Returns the product of the differences of 1 and 3 jolts"""
    one_diff = three_diff = 0

    for index in range(1, len(inputs)):
        diff = inputs[index] - inputs[index-1]
        one_diff = one_diff + 1 if diff == 1 else one_diff
        three_diff = three_diff + 1 if diff == 3 else three_diff

    return one_diff * three_diff


def count_adapter_arrangements(inputs, start_index, visited):
    """Returns the count of possible adapter arrangements"""
    next_possible_starts = []
    arrangements = 0

    if start_index == len(inputs) - 1:
        return 1

    curr_adapter = inputs[start_index]
    i = 1

    while start_index+i < len(inputs) and inputs[start_index+i] - curr_adapter <= 3:
        next_possible_starts.append(start_index+i) 
        i += 1

    for possible_start in next_possible_starts:
        if possible_start in visited.keys():
            arrangements += visited[possible_start]
        else:
            arrangements += count_adapter_arrangements(inputs, possible_start, visited)
            visited[possible_start] = arrangements

    return arrangements


def main():
    """Main function"""
    args = parse_arguments()
    
    inputs = get_inputs(args.input_file)
    
    ####################
    #      Part 1      #
    ####################
    jolt_diff_product = get_jolt_diff_product(inputs)
    print("[Part 1]\nProduct of Jolt Differences: {}\n".format(jolt_diff_product))
    
    ####################
    #      Part 2      #
    ####################
    num_arrangements = count_adapter_arrangements(inputs, 0, {})
    print("[Part 2]\nNumber of Adapter Arrangements: {}".format(num_arrangements))

if __name__ == "__main__":
    main()