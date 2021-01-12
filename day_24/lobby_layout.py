from collections import defaultdict
import copy
import numpy as np
import argparse


def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    instructions = []

    for idx, line in enumerate(inputs):
        instructions.append([])
        direction = ""
        for char in line:
            direction += char
            if char[-1] in 'ew':
                instructions[idx].append(direction)
                direction = ""

    return instructions


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


# directions are [e, ne, nw, w, sw, se]
DIRECTIONS = np.array([[1, -1, 0], [1, 0, -1], [0, 1, -1], [-1, 1, 0], [-1, 0, 1], [0, -1, 1]])


def flip_tiles(instructions):
    """Flip the tiles according to instructions"""
    tiles = defaultdict(bool)

    for instruction in instructions:
        coord = np.array([0, 0, 0])

        for move in instruction:
            if move == 'e':
                coord = np.add(coord, DIRECTIONS[0])
            elif move == 'ne':
                coord = np.add(coord, DIRECTIONS[1])
            elif move == 'nw':
                coord = np.add(coord, DIRECTIONS[2])
            elif move == 'w':
                coord = np.add(coord, DIRECTIONS[3])
            elif move == 'sw':
                coord = np.add(coord, DIRECTIONS[4])
            elif move == 'se':
                coord = np.add(coord, DIRECTIONS[5])
        
        coord_str = " ".join(str(x) for x in coord)
        tiles[coord_str] = not tiles[coord_str]
        
    return tiles


def get_adj_tiles(tile):
    """Return a list of adjacent tiles"""
    coord = np.fromstring(tile, dtype=int, sep=' ')
    adj_tiles = []
    
    for direction in DIRECTIONS:
        adj_tiles.append(" ".join(str(coord[i] + direction[i]) for i in range(3)))

    return adj_tiles


def tile_art(tiles, days=100):
    """Execute art exhibit for specified days"""

    def sort_adjs(adj_tiles):
        black_adjs = []
        white_adjs = []
        
        for adj_tile in adj_tiles:
            if adj_tile in tiles and tiles[adj_tile]:
                black_adjs.append(adj_tile)
            else:
                white_adjs.append(adj_tile)
        return black_adjs, white_adjs

    def check_white_adjs(adj_tiles):
        to_flip = []
        for adj_tile in adj_tiles:
            white_adjs = get_adj_tiles(adj_tile)
            black_adjs, _ = sort_adjs(white_adjs)
            if len(black_adjs) == 2:
                to_flip.append(adj_tile)

        return to_flip

    for _ in range(days):
        tile_copy = copy.copy(tiles)
        
        for tile in tiles:
            if tiles[tile]:
                adj_tiles = get_adj_tiles(tile)
                black_adjs, white_adjs = sort_adjs(adj_tiles)
                num_black_adjs = len(black_adjs)
                if not num_black_adjs or num_black_adjs > 2:
                    tile_copy[tile] = False
                # TODO: Slow runtime caused by checking all adjacents every iteration.
                #       Possibly save each tile's neighbor state before every iteration.
                to_flip = check_white_adjs(white_adjs)
                for flip_white in to_flip:
                    tile_copy[flip_white] = True
        tiles = tile_copy
        
    return tiles


def count_black_tiles(tiles):
    """Returns the number of black tiles"""
    flipped_tiles = 0

    for tile in tiles:
        flipped_tiles = flipped_tiles + 1 if tiles[tile] else flipped_tiles

    return flipped_tiles


def main():
    """Main function"""
    args = parse_arguments()
    
    instructions = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    tiles = flip_tiles(instructions)
    num_black_tiles = count_black_tiles(tiles)
    print("[Part 1]Number of Black Tiles: {}\n".format(num_black_tiles))

    ####################
    #      Part 2      #
    ####################
    tiles = tile_art(tiles, days=100)
    num_black_tiles = count_black_tiles(tiles)
    print("[Part 2]Number of Black Tiles: {}".format(num_black_tiles))
    

if __name__ == "__main__":
    main()