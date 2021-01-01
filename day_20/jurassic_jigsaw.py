from collections import defaultdict
import argparse
import numpy as np


class Tile:
    def __init__(self, id, tile_data):
        self.id = id
        self.width = len(tile_data)
        self.image = self.create_image(tile_data)
        self.sides = self.get_sides() # [top, right, bot, left]


    def create_image(self, tile_data):
        """Creates a tile image from its raw data"""
        image = np.empty([self.width, self.width], dtype=str)
        
        for index, line in enumerate(tile_data):
            np.copyto(image[index], list(line))

        return image
    
    def get_sides(self):
        """Returns the sides of the tile"""
        top = "".join(self.image[0])
        bot = "".join(self.image[-1])[::-1]
        left = "".join(self.image[:,0:1].flatten())[::-1]
        right = "".join(self.image[:,-1:].flatten())

        return [top, right, bot, left]

    def invert(self):
        """Inverts the tile"""
        self.rotate()
        self.image = np.flip(self.image, axis=0)
        self.sides = self.get_sides()
    
    def flip_side(self):
        """Flips the tile side to side"""
        self.image = np.flip(self.image, 1)
        self.sides = self.get_sides()

    def rotate(self, direction='cw'):
        """Rotates a tile"""
        if direction == 'cw':
            self.image = np.rot90(self.image, axes=(1,0))
        elif direction == 'cc':
            self.image = np.rot90(self.image)
        self.sides = self.get_sides()


class Jigsaw:
    def __init__(self, tiles):
        self.puzzle_width = int(np.sqrt(len(tiles)))
        self.tiles = tiles
        self.puzzle = np.empty([self.puzzle_width, self.puzzle_width], dtype=object)
        self.solve_puzzle()
        self.create_full_picture()

    def rotate_board(self):
        """Rotates the board and all of its tiles"""
        self.puzzle = np.rot90(self.puzzle)
        for row in self.puzzle:
            for col in row:
                if col is not None:
                    col.rotate(direction='cc')

    def flip_pieces(self):
        """Flips the board in case wrong orientation, should only be called once"""
        for row in self.puzzle:
            for col in row:
                if col is not None:
                    col.flip_side()

    def is_match(self, ref_tile, comp_tile):
        """Quick check whether the the tiles fit each other"""
        for i in range(4):
            if comp_tile.sides[i] in ref_tile.sides or comp_tile.sides[i][::-1] in ref_tile.sides:
                return i
        return -1

    def get_num_matching_sides(self, ref_tile):
        """Returns the number of sides that match the tile"""
        num_match = 0

        for tile in self.tiles:
            if tile == ref_tile:
                continue
            else:
                num_match = num_match + 1 if self.is_match(ref_tile, tile) >= 0 else num_match

        return num_match

    def get_corner(self):
        """Finds a corner piece"""
        for tile in self.tiles:
            if self.get_num_matching_sides(tile) <= 2:
                return tile

    def pop_tile(self, tile_id):
        """Pops a tile off its list based on its ID"""
        self.tiles = [tile for tile in self.tiles if tile.id != tile_id]
        
    def try_tile(self, tile_ref, tile_comp):
        """Tries to fit a tile to the left of one"""
        if tile_ref.id == tile_comp.id:
            return False

        for _ in range(2):
            for _ in range(4):
                if tile_ref.sides[1] == tile_comp.sides[3][::-1]:
                    return True
                tile_comp.rotate()
            tile_comp.invert()

        return False

    def find_right_match(self, tile_ref):
        """Finds the matching tile to its right"""
        for _ in range(2): # Flip at least once
            for tile in self.tiles:
                if self.try_tile(tile_ref, tile):
                    return tile
            self.flip_pieces()

        return None

    def solve_puzzle(self):
        """Solve the puzzle by arranging tiles properly
            
            Algorithm: The algorithm revolves around solving a corner, then the border. 
                       Once the border is complete, solve the next inner layer, until one
                       piece remains.

                1. Find a corner
                2. Place a corner piece on the board
                3. Try to find a matching tile with its previous tile
                4. If no more matches, one side of border is complete, rotate the board
                5. Once board has rotated 4 times, repeat steps with the next inner layer
        """
        layer = 0
        while len(self.tiles):
            corner = self.get_corner()
            self.pop_tile(corner.id)
            if self.puzzle[layer][layer] is None:
                if not layer:
                    self.puzzle[layer][layer] = corner
                else:
                    for _ in range(4):
                        if self.try_tile(self.puzzle[layer][layer-1], corner):
                            self.puzzle[layer][layer] = corner
                            break
                        self.rotate_board()
            for _ in range(4):
                for i in range(1, len(self.puzzle[0])-2*layer):
                    right_match = self.find_right_match(self.puzzle[layer][layer+i-1])
                    if right_match is None:
                        break
                    self.puzzle[layer][layer+i] = right_match
                    self.pop_tile(right_match.id)
                self.rotate_board()
            layer += 1

    def create_full_picture(self):
        """Creates the full picture from the solved puzzle and removed borders"""
        tile_width = self.puzzle[0][0].width - 2
        full_picture_width = self.puzzle_width * tile_width
        full_picture = np.empty([full_picture_width, full_picture_width], dtype=str)

        for row in range(len(self.puzzle)):
            for col in range(len(self.puzzle[0])):
                full_picture[row*tile_width:row*tile_width+tile_width,col*tile_width:col*tile_width+tile_width] = self.puzzle[row][col].image[1:-1,1:-1]

        self.full_picture = full_picture

    def rotate_picture(self):
        """Rotates the picture"""
        self.full_picture = np.rot90(self.full_picture)

    def invert_picture(self):
        """Inverts the picture"""
        self.full_picture = np.flip(np.rot90(self.full_picture), axis=0)

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')
    parser.add_argument('--monster', '-m', help='Path to the monster file.', default='monster.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    tiles = []
    
    for i in range(0, len(inputs), 12):
        tile_id = inputs[i].split(':')[0]
        tiles.append(Tile(tile_id, inputs[i+1:i+11]))
    
    return tiles


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def get_monster(monster_file):
    """Returns the 2d array of the monster"""
    monster = []

    with open(monster_file, 'r') as infile:
        monster = infile.read().splitlines()

    return monster

def get_monster_indices(monster):
    """Returns a list of indices of the monster"""
    indices = []
    for row in range(len(monster)):
        for col in range(len(monster[0])):
            if monster[row][col] == '#':
                indices.append((row, col))

    return indices

def get_corner_tiles_product(jigsaw):
    """Returns the product of the corners' tile IDs"""
    corners = [jigsaw.puzzle[0,0].id, jigsaw.puzzle[0,-1].id, jigsaw.puzzle[-1,0].id, jigsaw.puzzle[-1,-1].id]
    corners = [int(x.split(" ")[1]) for x in corners]

    product = 1
    for corner in corners:
        product *= corner

    return product

def get_monsters_units(jigsaw, monster):
    """Returns the number of #'s belonging to monsters"""
    num_monsters = 0
    height = len(monster)
    length = len(monster[0])
    indices = get_monster_indices(monster)

    for _ in range(2):
        for _ in range(4):
            for row in range(len(jigsaw.full_picture)-height):
                for col in range(len(jigsaw.full_picture[0])-length):
                    for index in indices:
                        if jigsaw.full_picture[row+index[0],col+index[1]] != '#':
                            break
                    else:
                        num_monsters += 1
            jigsaw.rotate_picture()
        jigsaw.invert_picture()

    return num_monsters * len(indices)

def count_waters(jigsaw, monster):
    """Returns the difference of all #'s and the ones of the monsters"""
    monster_size = get_monsters_units(jigsaw, monster)
    _values, occurences = np.unique(jigsaw.full_picture, return_counts=True)
    
    return occurences[0] - monster_size


def main():
    """Main function"""
    args = parse_arguments()
    
    tiles = get_inputs(args.input_file)
    monster = get_monster(args.monster)
    
    jig = Jigsaw(tiles)

    ####################
    #      Part 1      #
    ####################
    corner_tiles_product = get_corner_tiles_product(jig)
    print("[Part 1]\nProduct of Corner Tiles: {}\n".format(corner_tiles_product))
    
    ####################
    #      Part 2      #
    ####################
    num_waters = count_waters(jig, monster)
    print("[Part 2]\nNumber of Waters: {}".format(num_waters))


if __name__ == "__main__":
    main()