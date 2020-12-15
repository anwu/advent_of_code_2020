import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    init_program = []

    for line in inputs:
        addr, value = line.split(' = ')
        init_program.append((addr, value))

    return init_program


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def apply_v1_bit_mask(init_program):
    """Get the init program sum using the v1 decoder"""
    or_bin_mask = 0
    and_bin_mask = 0
    memory = {}

    for address, value in init_program:
        if address == 'mask':
            or_bin_mask = int(value.replace('X', '0'), 2)
            and_bin_mask = int(value.replace('X', '1'), 2)
            continue
        memory[address] = int(value) | or_bin_mask
        memory[address] &= and_bin_mask

    return sum(memory.values())


def get_mask_addresses(mask, address):
    """Get all possible addresses based on the mask"""
    addresses = []
    new_mask = '{0:036b}'.format(int(address.strip("mem[]")) | int(mask.replace('X', '0'), 2))

    floating_bit_indices = [i for i in range(len(mask)) if mask.startswith('X', i)]

    for i in range(2 ** len(floating_bit_indices)):
        address = list(new_mask)
        for index, bit in enumerate(floating_bit_indices):
            address[bit] = str(((i >> index) & 1))
        addresses.append("".join(address))

    return addresses

def apply_v2_bit_mask(init_program):
    """Get the sum of the init program using the v2 decoder"""
    memory = {}

    for address, value in init_program:
        if address == 'mask':
            mask = value
            continue
        addresses = get_mask_addresses(mask, address)
        for address in addresses:
            memory[address] = int(value)

    return sum(memory.values())


def main():
    """Main function"""
    args = parse_arguments()
    
    init_program = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    init_program_sum = apply_v1_bit_mask(init_program)
    print("[Part 1]\nInit Program's Sum: {}\n".format(init_program_sum))

    ####################
    #      Part 2      #
    ####################
    init_program_sum = apply_v2_bit_mask(init_program)
    print("[Part 2]\nInit Program's Sum: {}".format(init_program_sum))


if __name__ == "__main__":
    main()