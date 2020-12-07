import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    colored_bags = {}

    for line in inputs:
        bag, contents = line.split(' bags contain ')
        contents = contents.split(', ')
        bag_contents = []
        for content in contents:
            num, sub_bag = content.split(' ', 1)
            bag_contents.append({'bag': sub_bag.split(' bag')[0], 'quantity': num})
        colored_bags[bag] = bag_contents
    # print(colored_bags)
    return colored_bags
    # returns dict(list(dict))
    # colored_bags = {
    #     'color_a': [
    #         {
    #             'bag': sub_bag,
    #             'quantity': num
    #         },
    #         {
    #             'bag': sub_bag,
    #             'quantity': num
    #         }
    #     ]
    # }


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def get_initial_valid_colors(colored_bags, key):
    """Returns a list of bags that contain the key bag"""
    valid_colors = []
    for bag_name, bag_contents in colored_bags.items():
        for content in bag_contents:
            if content['bag'] == key:
                valid_colors.append(bag_name)

    return valid_colors


def get_num_valid_bag_colors(colored_bags, key):
    """Gets the number of bags that eventually contain the key bag"""
    search_colors = valid_colors = get_initial_valid_colors(colored_bags, key)
    
    while search_colors:
        new_valid_colors = []
        for color in search_colors:
            new_valid_colors += get_initial_valid_colors(colored_bags, color)
        valid_colors += new_valid_colors
        search_colors = new_valid_colors

    valid_colors = list(set(valid_colors))

    return len(valid_colors)


def get_num_required_bags(colored_bags, key):
    """Recursively search and return the required number of bags based on key"""
    num_required_bags = 0

    if colored_bags[key][0]['quantity'] == 'no':
        return num_required_bags

    for content in colored_bags[key]:
        num_required_bags += int(content['quantity'])
        num_required_bags += get_num_required_bags(colored_bags, content['bag']) * int(content['quantity'])

    return num_required_bags

def main():
    """Main function"""
    args = parse_arguments()
    
    colored_bags = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    num_valid_bag_colors = get_num_valid_bag_colors(colored_bags, 'shiny gold')
    print("[Part 1]\nNumber of Bag Colors with Shiny Gold Bag: {}\n".format(num_valid_bag_colors))
    
    ####################
    #      Part 2      #
    ####################
    num_required_bags = get_num_required_bags(colored_bags, 'shiny gold')
    print("[Part 2]\nNumber of Required Bags in Shiny Gold Bag: {}".format(num_required_bags))

if __name__ == "__main__":
    main()