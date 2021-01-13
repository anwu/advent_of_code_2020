import argparse
import cProfile

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    return int(inputs[0]), int(inputs[1])


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def calc_encryption_key(pub_key, loop_size):
    val = 1

    for _ in range(loop_size):
        val *= pub_key
        val %= 20201227
    
    return val


def get_encryption_key(key1, key2):
    def get_min_loop_and_key():
        loop_size = 0
        val = 1

        while True:
            loop_size += 1
            val *= 7
            val %= 20201227
            if val == key1:
                return loop_size, key2
            if val == key2:
                return loop_size, key1

    loop_size, key = get_min_loop_and_key()

    return calc_encryption_key(key, loop_size)


def main():
    """Main function"""
    args = parse_arguments()
    
    door_pub, card_pub = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    encryption_key = get_encryption_key(door_pub, card_pub)
    print("[Part 1]\nEncryption Key: {}\n".format(encryption_key))
    
    ####################
    #      Part 2      #
    ####################
    

if __name__ == "__main__":
    # main()
    cProfile.run('main()')