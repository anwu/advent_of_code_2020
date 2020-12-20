import argparse
import pyparsing

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs, part):
    for i in range(len(inputs)):
        inputs[i] = "(" + inputs[i] + ")"

    return inputs


def get_inputs(input_file, part=1):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs, part)

    return inputs


def calculate_expression(expression):
    """Calculates the expression and return its value"""
    ops = 0 # 0 is equal, 1 is add, 2 is multiply
    res = 0
    
    def _calculate_ops(operator, operand, res):
        """Actual function to calculate operators with operands"""
        if operator == 0:
            res = operand
        elif operator == 1:
            res += operand
        else:
            res *= operand
        return res

    while len(expression):
        op = expression.pop(0)
        if isinstance(op, list):
            sub_exp = calculate_expression(op)
            res = _calculate_ops(ops, int(sub_exp), res)
        elif op == '+':
            ops = 1
        elif op == '*':
            ops = 2
        else:
            res = _calculate_ops(ops, int(op), res)

    return res


def get_sum_of_expressions(expressions, part=1):
    """Returns sum of expressions while using pyparsing to choose order of operations"""
    if part == 1: # No order of operation
        expr = pyparsing.nestedExpr(ignoreExpr=None)
    else: # Addition is first in order of operations
        expr = pyparsing.infixNotation(pyparsing.Word(pyparsing.alphanums),
                                    [
                                        ("+", 2, pyparsing.opAssoc.LEFT),
                                        ("*", 2, pyparsing.opAssoc.LEFT)
                                    ])
    expressions_sum = 0

    for expression in expressions:
        exp_sum = calculate_expression(expr.parseString(expression).asList())
        expressions_sum += exp_sum

    return expressions_sum


def main():
    """Main function"""
    args = parse_arguments()
    
    expressions = get_inputs(args.input_file)
    
    ####################
    #      Part 1      #
    ####################
    expressions_sum = get_sum_of_expressions(expressions)
    print("[Part 1]\nSum of Expressions: {}\n".format(expressions_sum))

    ####################
    #      Part 2      #
    ####################
    expressions = get_inputs(args.input_file)
    expressions_sum = get_sum_of_expressions(expressions, part=2)
    print("[Part 2]\nSum of Expressions: {}".format(expressions_sum))
    

if __name__ == "__main__":
    main()