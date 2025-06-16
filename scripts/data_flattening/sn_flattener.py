import json
import argparse
from itso_ai.parsers import servicenow


def main():
    parser = argparse.ArgumentParser(description='ServiceNow Ticket Flattener')
    parser.add_argument('-i', '--input', required=True,
                        help='JSON ServiceNow Ticket file from sn_crawler.py output')
    parser.add_argument('-o', '--output', required=True,
                        help='Output filename')
    parser.add_argument('-t', '--template-dir', required=True,
                        help='Directory containing output template files')
    args = parser.parse_args()

    f_in = open(args.input, 'r')
    f_out = open(args.output, 'w')
    ticket_template = open('%s/ticket.template' % args.template_dir, 'r').read()

    for line in f_in.readlines():
        ticket_dict = json.loads(line).get('ticket')
        ticket = servicenow.SNParser(ticket_template)
        ticket.process_ticket(ticket_dict)
        f_out.write(ticket.to_string() + '\n\n')

    f_in.close()
    f_out.close()
    return


if __name__ == '__main__':
    main()
