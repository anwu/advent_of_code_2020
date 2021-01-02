from collections import defaultdict
from functools import reduce
import numpy as np
import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    foods = []
    for line in inputs:
        ingredients, allergens = line.replace('(', '').replace(')', '').split(' contains ')
        foods.append((ingredients.split(' '), allergens.split(', ')))

    return foods


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def categorize_foods(foods):
    """Return a dict of allergies with list of foods that they are in"""
    cat_food = defaultdict(list)

    for food in foods:
        for allergen in food[1]:
            cat_food[allergen].append(food[0])
    
    return cat_food


def find_allergen_intersects(cat_food):
    """Returns allergy definitions using boolean operations to find set intersects and differences"""
    allergen_defs = defaultdict(list)
    solved = []

    # Find at least one known allergy by finding intersects of lists of an allergy
    for allergy in cat_food:
        allergen_defs[allergy] = reduce(np.intersect1d, cat_food[allergy])
        if len(allergen_defs[allergy]) == 1:
            solved.append(allergen_defs[allergy][0])

    # Use the other known allergies to find the remaining allergies
    while len(solved) != len(allergen_defs):
        for allergy in allergen_defs:
            if len(allergen_defs[allergy]) == 1:
                continue
            allergen_defs[allergy] = np.setdiff1d(allergen_defs[allergy], np.intersect1d(allergen_defs[allergy], solved))
            if len(allergen_defs[allergy]) == 1:
                solved.append(allergen_defs[allergy][0])

    return allergen_defs


def get_non_allergen_count(foods, allergen_defs):
    """Counts the number of non allergen ingredients in the foods"""
    allergen_list = [allergen_defs[allergy][0] for allergy in allergen_defs]
    num_non_allergen = 0

    for food in foods:
        num_non_allergen += len(np.setdiff1d(food[0], allergen_list))

    return num_non_allergen


def sort_allergen_list(allergen_defs):
    """Return a list of sorted dictionary items"""
    return [allergen[1][0] for allergen in sorted(allergen_defs.items())]


def main():
    """Main function"""
    args = parse_arguments()
    
    foods = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    cat_food = categorize_foods(foods)
    allergen_defs = find_allergen_intersects(cat_food)
    num_non_allergens = get_non_allergen_count(foods, allergen_defs)
    print("[Part 1]\nNumber of Non-Allergens: {}\n".format(num_non_allergens))

    ####################
    #      Part 2      #
    ####################
    sorted_allergen_list = sort_allergen_list(allergen_defs)
    print("[Part 2]\nAllergen List: {}".format(",".join(sorted_allergen_list)))
    

if __name__ == "__main__":
    main()