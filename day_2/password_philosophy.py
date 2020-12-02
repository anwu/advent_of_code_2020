import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.')

    return parser.parse_args()


def _normalize_inputs(inputs):
    parsed_inputs = []

    for line in inputs:
        bounds, letter, password = line.split(' ')
        lower_bound, upper_bound = bounds.split('-')
        letter = letter.strip(':')
        parsed_input = {
            'lower_bound': int(lower_bound),
            'upper_bound': int(upper_bound),
            'letter': letter,
            'password': password
            }
        parsed_inputs.append(parsed_input)

    return parsed_inputs


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs

def p1_count_valid_passwords(inputs):
    """Returns the number of valid passwords.
    
    A password is valid if it contains at least `lower_bound` and 
    at most `upper_bound` number of the `letter` in the `password`.
    """
    count = 0

    for entry in inputs:
        num_occurrences = entry['password'].count(entry['letter'])
        if (num_occurrences >= entry['lower_bound'] and
            num_occurrences <= entry['upper_bound']):
            count += 1

    return count


def p2_count_valid_passwords(inputs):
    """Returns the number of valid passwords.
    
    A password is valid only if one character at either the `lower_bound`
    or `upper_bound` position of the `password` is `letter`.
    """
    count = 0

    for entry in inputs:
        if entry['lower_bound'] <= 0:
            lower_letter = None
        else:
            lower_letter = entry['password'][entry['lower_bound']-1]

        if len(entry['password']) < entry['upper_bound']:
            upper_letter = None
        else:
            upper_letter = entry['password'][entry['upper_bound']-1]

        lower = True if lower_letter == entry['letter'] else False
        upper = True if upper_letter == entry['letter'] else False

        valid = lower ^ upper
        if valid:
            count += 1

    return count

def main():
    """Main function"""
    args = parse_arguments()
    
    inputs = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    num_valid_passwords = p1_count_valid_passwords(inputs)
    print("[Part 1]\nNumber of valid passwords: {}\n".format(num_valid_passwords))

    ####################
    #      Part 2      #
    ####################
    num_valid_passwords = p2_count_valid_passwords(inputs)
    print("[Part 2]\nNumber of valid passwords: {}".format(num_valid_passwords))
    

if __name__ == "__main__":
    main()