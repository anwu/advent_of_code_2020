import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    group_answers = []
    answers = ""

    for line in inputs:
        if not line:
            group_answers.append(answers[:-1])
            answers = ""
        else:
            answers += line + ' ' # add space to make parsing entries easier
    group_answers.append(answers[:-1]) # removing last whitespace

    return group_answers


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def p1_get_sum_of_counts(group_answers):
    """Gets the count of all unique characters in the entry"""
    sum = 0
    
    for answers in group_answers:
        answer = answers.replace(' ', '')
        count = len("".join(set(answer)))
        sum += count

    return sum


def p2_get_sum_of_counts(group_answers):
    """Gets the count of all duplicate characters"""
    sum = 0

    for answers in group_answers:
        entries = answers.split(' ')
        longest_entry = max(entries, key=len)
        for question in longest_entry:
            if answers.count(question) == len(entries):
                sum += 1

    return sum


def main():
    """Main function"""
    args = parse_arguments()
    
    group_answers = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    sum_of_counts = p1_get_sum_of_counts(group_answers)
    print("[Part 1]\nSum of Counts: {}\n".format(sum_of_counts))
    
    ####################
    #      Part 2      #
    ####################
    sum_of_counts = p2_get_sum_of_counts(group_answers)
    print("[Part 2]\nSum of Counts: {}".format(sum_of_counts))


if __name__ == "__main__":
    main()