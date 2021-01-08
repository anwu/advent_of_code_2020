from collections import deque
import numpy as np
import cProfile
import argparse

class CupCircle:
    def __init__(self):
        self.head = None

class Cup:
    def __init__(self, idx):
        self.idx = idx
        self.next = None

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    # return deque([int(x) for x in inputs[0]])
    return np.array([int(x) for x in inputs[0]])


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def play_crab_cups(cups, moves=100):
    """Plays Crab Cups and returns the end cups"""
    min_cup = min(cups)
    max_cup = max(cups)
    curr = cups[0]
    next_cups = list(range(1, len(cups)+2))

    # The index of next_cups is the cup itself, where its value is its next cup
    for idx in range(len(cups)):
        next_cups[cups[idx]] = cups[(idx+1)%len(cups)]

    for _ in range(moves):
        dest_cup = curr - 1
        picked_cup1 = next_cups[curr]
        picked_cup2 = next_cups[picked_cup1]
        picked_cup3 = next_cups[picked_cup2]
        
        while dest_cup in [picked_cup1, picked_cup2, picked_cup3] or dest_cup < min_cup:
            if dest_cup <= min_cup:
                dest_cup = max_cup
            else:
                dest_cup -= 1
        
        next_cups[curr] = next_cups[picked_cup3]
        next_cups[picked_cup3] = next_cups[dest_cup]
        next_cups[dest_cup] = picked_cup1
        curr = next_cups[curr]

    return next_cups

def get_end_cup_labels(cups):
    """Returns the cup labels after cup 1 after playing Crab Cups"""
    end_cups = play_crab_cups(cups, moves=100)
    
    cup_labels = ""
    idx = 1
    for _ in range(len(cups)-1):
        idx = end_cups[idx]
        cup_labels += str(idx)
    
    return cup_labels


def get_product_star_cups(cups):
    """Returns the product of the two cups clockwise of cup 1 after playing Crab Cups"""
    cups = np.concatenate((cups, np.arange(len(cups)+1, 1000001)))

    end_cups = play_crab_cups(cups, moves=10000000)
    star_cup1 = end_cups[1]
    star_cup2 = end_cups[star_cup1]

    return int(star_cup1) * int(star_cup2)


def main():
    """Main function"""
    args = parse_arguments()
    
    cups = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    cup_labels = get_end_cup_labels(cups)
    print("[Part 1]\nCup Labels: {}\n".format(cup_labels))

    ####################
    #      Part 2      #
    ####################
    star_cup_prod = get_product_star_cups(cups)
    print("[Part 2]\nProduct of Star Cups: {}".format(star_cup_prod))
    

if __name__ == "__main__":
    main()
    # cProfile.run('main()')