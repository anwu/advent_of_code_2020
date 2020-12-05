import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    passports = []  
    entry = {}

    for line in inputs:
        if not line:
            passports.append(entry)
            entry = {}
        else:
            pairs = line.split(' ')
            for pair in pairs:
                key, value = pair.split(':')
                entry[key] = value

    passports.append(entry)

    return passports


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def p1_get_num_valid_passports(passports):
    """Gets the number of valid passports for part 1"""
    num_valid_entries = 0

    for entry in passports:
        if len(entry) == 8:
            num_valid_entries += 1
        elif len(entry) == 7 and 'cid' not in entry.keys():
            num_valid_entries += 1

    return num_valid_entries


def check_year(year, min_year, max_year):
    """Checks if the year is within the valid range"""
    year = int(year) if not isinstance(year, int) else year
    return year >= min_year and year <= max_year


def check_height(height_entry):
    """Checks that the height is a valid number and unit"""
    try:
        height_num = int(height_entry[:-2])
    except:
        return False
    height_unit = height_entry[-2:]

    if height_unit == 'cm':
        return height_num >= 150 and height_num <= 193
    elif height_unit == 'in':
        return height_num >= 59 and height_num <= 76
    return False


def check_hair_color(hair_color_entry):
    """Checks that the hair color is a valid hex value prepended by #"""
    if hair_color_entry[0] != '#' and len(hair_color_entry) != 7:
        return False

    try:
        int(hair_color_entry[1:], 16)
    except:
        return False
    return True


def check_eye_color(eye_color_entry):
    """Checks that the eye color is within the known list"""
    valid_colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    return eye_color_entry in valid_colors


def check_passport(passport_entry):
    """Checks that the passport id is 9 digits long"""
    return passport_entry.isdigit() and len(passport_entry) == 9


def check_rules(key, value):
    """Switch statement to check for each field"""
    if key == 'byr':
        return check_year(value, 1920, 2002)
    elif key == 'iyr':
        return check_year(value, 2010, 2020)
    elif key == 'eyr':
        return check_year(value, 2020, 2030)
    elif key == 'hgt':
        return check_height(value)
    elif key == 'hcl':
        return check_hair_color(value)
    elif key == 'ecl':
        return check_eye_color(value)
    elif key == 'pid':
        return check_passport(value)
    elif key == 'cid':
        return True
    else:
        return False


def p2_get_num_valid_passports(passports):
    """Gets the number of valid passports for part 2"""
    num_valid_entries = 0
    result = False

    for entry in passports:
        if (len(entry) == 7 and 'cid' in entry.keys()) or len(entry) < 7:
            continue

        for key, value in entry.items():
            result = check_rules(key, value)
            if not result:
                break

        if result is True:
            num_valid_entries += 1

    return num_valid_entries


def main():
    """Main function"""
    args = parse_arguments()
    
    passports = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    num_valid_passports = p1_get_num_valid_passports(passports)
    print("[Part 1]\nNumber of Valid Passports: {}\n".format(num_valid_passports))
    
    ####################
    #      Part 2      #
    ####################
    num_valid_passports = p2_get_num_valid_passports(passports)
    print("[Part 2]\nNumber of Valid Passports: {}".format(num_valid_passports))

if __name__ == "__main__":
    main()