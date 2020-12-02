import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.')

    return parser.parse_args()


def _normalize_inputs(inputs):
    inputs = [int(input) for input in inputs]
    return inputs


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def get_entries_of_sum(inputs, num_entries, sum, entries=[]):
    """Recursive function to return a list of entries of a sum given by the parameter"""
    if num_entries == 1:
        if sum in inputs:
            entries.append(sum)
            return entries
        return None
    
    for input in inputs:
        diff = sum - input
        new_inputs = inputs.copy()
        new_inputs.remove(input)
        entries = get_entries_of_sum(new_inputs, num_entries-1, diff, entries)
        if entries is not None:
            entries.append(input)
            return entries
        else:
            entries = []

    return None

def get_product_of_entries(entries):
    """Simple operation to find the product of a list"""
    product = 1

    for entry in entries:
        product *= entry

    return product


def main():
    """Main function"""
    args = parse_arguments()
    
    inputs = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    entries = get_entries_of_sum(inputs, 2, 2020)
    product = get_product_of_entries(entries)
    print("Entries: {}\nProduct: {}\n".format(entries, product))

    ####################
    #      Part 2      #
    ####################
    entries = get_entries_of_sum(inputs, 3, 2020)
    product = get_product_of_entries(entries)
    print("Entries: {}\nProduct: {}\n".format(entries, product))


if __name__ == "__main__":
    main()