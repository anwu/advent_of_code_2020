from collections import defaultdict
import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    rules = defaultdict(list)
    line_break = inputs.index('')

    # Separate subrules by |, as individual list elements
    for rule in inputs[:line_break]:
        rule_id, rule_val = rule.split(': ')
        for rule_list in rule_val.split(' | '):
            rules[rule_id].append(rule_list.replace('"', '').split(' '))
    messages = inputs[line_break+1:]
    return rules, messages


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def message_is_valid(rule_id, rules, message):
    """Checks if message is valid, -1 if not, otherwise the length of message"""
    if not len(message):
        return -1

    # Base case
    if rules[rule_id] == [['a']] or rules[rule_id] == [['b']]:
        if message[0] == rules[rule_id][0][0]:
            return 1
        else:
            return -1

    for sub_list in rules[rule_id]:
        count = 0
        for sub_rule in sub_list:
            res = message_is_valid(sub_rule, rules, message[count:])
            if res > 0:
                count += res
            else:
                break
        else:
            return count
    return -1

# Example
# 31
# 14 17
# b 14 2
# b b 1 24
# b b a 14 1
# b b a b 1
# last section has to be length of 5

# Actual input
# 31 
# 43 44
# a 88 43
# a 43 26 a
# a a 35 38 a
# a a b 35 56 a
# a a b b 14 35 a
# a a b b 35 35 b a
# a a b b b b b a
# last section has to be length of 8
#
# 42
# 43 106
# a 33 43
# a 96 43 a
# a 35 127 a a
# a b 43 110 a a
# a b a 43 92 a a
# a b a a 35 43 a a
# a b a a b a a a
# last section is length of 8 as well

def get_num_msgs_match_rule(rules, messages, part=1):
    """Returns the total number of messages that match the rules"""
    num_valid_msgs = 0

    for message in messages:
        if part == 1:
            if message_is_valid("0", rules, message) == len(message):
                num_valid_msgs += 1
        else:
            sub_messages = [message[i:i+8] for i in range(0, len(message), 8)]

            for n in range(1, (len(sub_messages) - 1) // 2 + 1):
                if all(
                    message_is_valid("42", rules, sub_msg) == len(sub_msg)
                    for sub_msg in sub_messages[:-n]
                ) and all(
                    message_is_valid("31", rules, sub_msg) == len(sub_msg)
                    for sub_msg in sub_messages[-n:]
                ):
                    num_valid_msgs += 1
                    break
    
    return num_valid_msgs


def main():
    """Main function"""
    args = parse_arguments()
    
    rules, messages = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    num_match_rule = get_num_msgs_match_rule(rules, messages)
    print("[Part 1]\nNumber of Messages Matching Rule 0: {}\n".format(num_match_rule))

    ####################
    #      Part 2      #
    ####################
    num_match_rule = get_num_msgs_match_rule(rules, messages, part=2)
    print("[Part 2]\nNumber of Messages Matching Rule 0: {}".format(num_match_rule))
    

if __name__ == "__main__":
    main()