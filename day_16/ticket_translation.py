import argparse

def parse_arguments():
    """Parses command line arguments"""
    parser = argparse.ArgumentParser(description='Loading inputs from a text file.')
    parser.add_argument('--input_file', '-i', help='Path to text input file.', default='input.txt')

    return parser.parse_args()


def _normalize_inputs(inputs):
    rules = {}
    nearby_tickets = []

    index = 0
    while inputs[index] != '':
        rule, ranges = inputs[index].split(': ')
        range1, range2 = ranges.split(' or ')
        range1 = tuple(int(x) for x in range1.split('-'))
        range2 = tuple(int(x) for x in range2.split('-'))
        rules[rule] = (range1, range2)
        index += 1
    
    my_ticket = [int(x) for x in inputs[index+2].split(',')]

    for i in range(index+5, len(inputs)):
        nearby_tickets.append([int(x) for x in inputs[i].split(',')])
    
    return rules, my_ticket, nearby_tickets


def get_inputs(input_file):
    """Return a list of inputs delimited by newlines"""
    inputs = []

    with open(input_file, 'r') as infile:
        inputs = [line.strip() for line in infile]

    inputs = _normalize_inputs(inputs)

    return inputs


def check_rule(rules, field):
    """Checks that the field follows at least one of the rules"""
    res = False

    for rule in rules:
        if (field >= rules[rule][0][0] and field <= rules[rule][0][1]) or (field >= rules[rule][1][0] and field <= rules[rule][1][1]):
            res = True

    return res


def get_ticket_error_rate(rules, tickets):
    """Gets the error rate from the invalid tickets"""
    invalid_tickets = []

    for index, ticket in enumerate(tickets):
        for field in ticket:
            if not check_rule(rules, field):
                invalid_tickets.append((index, field))

    invalid_tickets.sort(key=lambda ticket: ticket[0], reverse=True)
    
    for ticket, _field in invalid_tickets:
        tickets.pop(ticket)

    return sum(x[1] for x in invalid_tickets)


def filter_fields(possible_fields):
    """Filters each possible field by process of elimination"""
    single_fields = []

    for index, line in enumerate(possible_fields):
        if len(line) == 1:
            single_fields.append((index, line[0]))
    
    for index, fields in enumerate(possible_fields):
        for i in range(len(single_fields)):
            if single_fields[i][1] in fields and index != single_fields[i][0]:
                fields.remove(single_fields[i][1])

    
def get_departures_product(rules, tickets, my_ticket):
    """Get the product of ticket fields starting with 'departures"""
    possible_fields = []
    i = 0

    while i < len(my_ticket):
        possible_fields.append([])
        for rule in rules:
            res = True
            for ticket in tickets:
                if (ticket[i] >= rules[rule][0][0] and ticket[i] <= rules[rule][0][1]) or (ticket[i] >= rules[rule][1][0] and ticket[i] <= rules[rule][1][1]):
                    pass
                else:
                    res = False
                    break
            if res:
                possible_fields[-1].append(rule)
        i += 1
    
    for i in range(len(rules)):
        filter_fields(possible_fields)

    departures_product = 1
    for index, field in enumerate(possible_fields):
        if field[0].startswith("departure"):
            departures_product *= my_ticket[index]
    
    return departures_product

def main():
    """Main function"""
    args = parse_arguments()
    
    rules, my_ticket, nearby_tickets = get_inputs(args.input_file)

    ####################
    #      Part 1      #
    ####################
    ticket_error_rate = get_ticket_error_rate(rules, nearby_tickets)
    print("[Part 1]\nTicket Error Rate: {}\n".format(ticket_error_rate))

    ####################
    #      Part 2      #
    ####################
    departures_product = get_departures_product(rules, nearby_tickets, my_ticket)
    print("[Part 2]\nProduct of Departure Fields: {}".format(departures_product))

if __name__ == "__main__":
    main()