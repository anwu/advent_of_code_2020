import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.')

    return parser.parse_args()


def _normalize_inputs(inputs):
    # TODO: Add operations to normalize inputs based on prompt
    return inputs


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def main():
    """Main function"""
    args = parse_arguments()
    
    inputs = get_inputs(args.input_file)

    # TODO: Add solution here
    

if __name__ == "__main__":
    main()