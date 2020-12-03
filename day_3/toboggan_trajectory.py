import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.')

    return parser.parse_args()


def _normalize_inputs(inputs):
    map = []

    for line in inputs:
        row = [ele for ele in line]
        map.append(row)
    
    return map


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def traverse_slope(map, col_inc=3, row_inc=1):
    """Traverse the 2d array in increasing order by given increments"""
    row = col = encountered_trees = 0
    right_bound = len(map[0])
    bottom_bound = len(map)

    while row < bottom_bound:
        if map[row][col] == '#':
            encountered_trees += 1
        row += row_inc
        col += col_inc
        col %= right_bound

    return encountered_trees


def main():
    """Main function"""
    args = parse_arguments()
    
    map = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    trees_encountered = traverse_slope(map)
    print("[Part 1]\nTrees Encountered: {}\n".format(trees_encountered))
    
    ####################
    #      Part 2      #
    ####################
    product = 1
    product *= traverse_slope(map, col_inc=1, row_inc=1)
    product *= traverse_slope(map, col_inc=3, row_inc=1)
    product *= traverse_slope(map, col_inc=5, row_inc=1)
    product *= traverse_slope(map, col_inc=7, row_inc=1)
    product *= traverse_slope(map, col_inc=1, row_inc=2)
    print("[Part 2]\nProduct of Encountered Trees: {}".format(product))


if __name__ == "__main__":
    main()