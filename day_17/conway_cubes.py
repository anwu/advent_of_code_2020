import argparse
import numpy as np
import sys

CYCLES_TO_BOOT = 6


def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs, ndim):
    x_len = len(inputs[0]) + CYCLES_TO_BOOT * 2
    y_len = len(inputs) + CYCLES_TO_BOOT * 2
    z_len = CYCLES_TO_BOOT * 2 + 1
    w_len = CYCLES_TO_BOOT * 2 + 1 if ndim == 4 else 1

    origin = (w_len//2, z_len//2, y_len//2, x_len//2)
    cube_state = np.full((w_len, z_len, y_len, x_len), '.')
    
    x_start = origin[3] - len(inputs[0]) // 2
    x_end = origin[3] + (len(inputs[0]) + 1) // 2
    y_start = origin[2] - len(inputs) // 2

    for index, line in enumerate(inputs):
        cube_state[origin[0]][origin[1]][y_start+index][x_start:x_end] = list(line)

    return cube_state


def get_inputs(input_file, ndim=3):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs, ndim)

    return inputs


def _within_bounds(w_min, w_max, z_min, z_max, y_min, y_max, x_min, x_max, w, z, y, x):

    if w >= w_min and w < w_max and z >= z_min and z < z_max and y >= y_min and y < y_max and x >= x_min and x < x_max:
        return True
    return False 


def get_active_neighbors(cube_state, coords):
    """Returns the number of active neighbors from a given coordinate"""
    w_max = len(cube_state)
    z_max = len(cube_state[0])
    y_max = len(cube_state[0][0])
    x_max = len(cube_state[0][0][0])
    num_active_neighbors = 0

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    w = coords[0] + i
                    z = coords[1] + j
                    y = coords[2] + k
                    x = coords[3] + l
                    if _within_bounds(0, w_max, 0, z_max, 0, y_max, 0, x_max, w, z, y, x) and not (i == 0 and j == 0 and k == 0 and l == 0):
                        num_active_neighbors = num_active_neighbors+1 if cube_state[w,z,y,x] == '#' else num_active_neighbors

    return num_active_neighbors


def get_active_count_after_boot(cube_state):
    """Simulates the boot cycle and returns the number of active cubes"""
    new_states = []
    w_size = len(cube_state)
    z_size = len(cube_state[0])
    y_size = len(cube_state[0][0])
    x_size = len(cube_state[0][0][0])
    num_active = 0

    for i in range(CYCLES_TO_BOOT):
        # Terrible runtime... probably a more efficient way to set up/reset structure and to
        # decide new state based on the active/inactive state of already calculated neighbors.
        # Just learned how to use numpy so I don't want to spend anymore time lol.
        for w in range(w_size):
            for z in range(z_size):
                for y in range(y_size):
                    for x in range(x_size):
                        num_active_neighbors = get_active_neighbors(cube_state, (w, z, y, x))
                        if cube_state[w, z, y, x] == '#':
                            if num_active_neighbors == 2 or num_active_neighbors == 3:
                                new_states.append('#')
                            else:
                                new_states.append('.')
                        else:
                            if num_active_neighbors == 3:
                                new_states.append('#')
                            else:
                                new_states.append('.')

        cube_state = np.array(new_states)
        cube_state = cube_state.reshape((w_size, z_size, y_size, x_size))

        if i == CYCLES_TO_BOOT - 1:
            num_active = new_states.count('#')
        new_states = []

    return num_active


def main():
    """Main function"""
    args = parse_arguments()
    
    initial_state = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    num_active_cubes = get_active_count_after_boot(initial_state)
    print("[Part 1]\nNumber of Active Cubes After Boot: {}\n".format(num_active_cubes))
    
    ####################
    #      Part 2      #
    ####################
    initial_state = get_inputs(args.input_file, ndim=4)
    num_active_cubes = get_active_count_after_boot(initial_state)
    print("[Part 2]\nNumber of Active Cubes After Boot: {}".format(num_active_cubes))


if __name__ == "__main__":
    main()