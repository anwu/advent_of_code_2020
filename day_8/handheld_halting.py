import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    instructions = []
    for line in inputs:
        operation, argument = line.split(' ')
        instructions.append([operation, int(argument)])

    return instructions


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def execute_instruction(line_count, instruction):
    """Returns the next instruction line number and value to increment accumulator"""
    next_instruction = line_count
    accumulator = 0

    if instruction[0] == 'acc':
        accumulator += instruction[1]
        next_instruction += 1
    elif instruction[0] == 'jmp':
        next_instruction += instruction[1]
    elif instruction[0] == 'nop':
        next_instruction += 1

    return next_instruction, accumulator


def get_accum_after_halt(instructions):
    """Execute each instruction until we see that instruction as already executed"""
    visited_instructions = []
    accumulator = 0
    next_instruction = 0

    while next_instruction not in visited_instructions:
        visited_instructions.append(next_instruction)
        next_instruction, accum = execute_instruction(next_instruction, instructions[next_instruction])
        accumulator += accum
        if next_instruction == len(instructions) and visited_instructions[-1] == len(instructions) - 1:
            return accumulator, next_instruction

    return accumulator, visited_instructions[-1]


def fix_program(instructions):
    """Iterate through potential fixes until the last line was executed"""
    accumulator = 0
    fix_attempt_count = 0
    last_instruction = 0

    while last_instruction != len(instructions):
        new_instruction = instructions[fix_attempt_count]
        old_instruction = new_instruction.copy()
        if new_instruction[0] != 'acc':
            new_instruction[0] = 'jmp' if new_instruction[0] == 'nop' else 'nop'
            instructions[fix_attempt_count] = new_instruction
            accumulator, last_instruction = get_accum_after_halt(instructions)
            instructions[fix_attempt_count] = old_instruction
        fix_attempt_count += 1

    return accumulator


def main():
    """Main function"""
    args = parse_arguments()
    
    instructions = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    accumulator_value, _ = get_accum_after_halt(instructions)
    print("[Part 1]\nAccumulator: {}\n".format(accumulator_value))

    ####################
    #      Part 2      #
    ####################
    accumulator_value = fix_program(instructions)
    print("[Part 2]\nAccumulator: {}".format(accumulator_value))

if __name__ == "__main__":
    main()