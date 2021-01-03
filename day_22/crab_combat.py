import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    cards = [int(line) for line in inputs if line.isnumeric()]

    return cards[:len(cards)//2], cards[len(cards)//2:]


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def play_combat(player1, player2):
    """Plays out a game of Combat and returns the winning hand"""
    while len(player1) and len(player2):
        p1_card = player1.pop(0)
        p2_card = player2.pop(0)
        if p1_card > p2_card:
            player1.append(p1_card)
            player1.append(p2_card)
        else:
            player2.append(p2_card)
            player2.append(p1_card)
    return player1 if len(player1) else player2


def play_recursive_combat(player1, player2):
    """Plays out a game of Recursive Combat and returns the winner and the hand"""
    p1_history = []
    while len(player1) and len(player2):
        p1_copy = player1.copy()
        p1_card = player1.pop(0)
        p2_card = player2.pop(0)

        if player1 in p1_history:
            return ('p1', player1)
        if p1_card <= len(player1) and p2_card <= len(player2):
            winner, _ = play_recursive_combat(player1[:p1_card], player2[:p2_card])
            if winner == 'p1':
                player1.append(p1_card)
                player1.append(p2_card)
            else:
                player2.append(p2_card)
                player2.append(p1_card)
        elif p1_card > p2_card:
            player1.append(p1_card)
            player1.append(p2_card)
        else:
            player2.append(p2_card)
            player2.append(p1_card)
        p1_history.append(p1_copy)
    return ('p1', player1) if len(player1) else ('p2', player2)


def get_winner_score(player1, player2, part=1):
    """Calculates the winning hand's score"""
    score = 0
    if part == 1:
        winner_hand = play_combat(player1, player2)
    else:
        _, winner_hand = play_recursive_combat(player1, player2)

    for index, card in enumerate(winner_hand[::-1]):
        score += (index + 1) * card

    return score

def main():
    """Main function"""
    args = parse_arguments()
    
    player1, player2 = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    score = get_winner_score(player1.copy(), player2.copy())
    print("[Part 1]Winner's Score: {}\n".format(score))

    ####################
    #      Part 2      #
    ####################
    score = get_winner_score(player1, player2, part=2)
    print("[Part 2]Winner's Score: {}".format(score))
    

if __name__ == "__main__":
    main()