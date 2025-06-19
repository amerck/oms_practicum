import json
import argparse
from itso_ai.parsers import servicenow


def flatten_ticket(ticket_dict):
    ticket_lines = []
    ticket = servicenow.SNParser(ticket_dict)
    ticket_body = json.dumps(ticket.get_ticket_body())
    ticket_lines.append(ticket_body)

    for work_note in ticket.get_work_notes():
        ticket_lines.append(json.dumps(work_note))
    return ticket_lines


def main():
    parser = argparse.ArgumentParser(description='ServiceNow Ticket Flattener')
    parser.add_argument('-i', '--input', required=True,
                        help='JSON ServiceNow Ticket file from sn_crawler.py output')
    parser.add_argument('-o', '--output', required=True,
                        help='Output filename')
    parser.add_argument('-t', '--template-dir', required=False,
                        help='Directory containing output template files')
    args = parser.parse_args()

    f_in = open(args.input, 'r')
    f_out = open(args.output, 'w')
    # ticket_template = open('%s/ticket.template' % args.template_dir, 'r').read()

    for line in f_in.readlines():
        ticket_dict = json.loads(line)
        ticket_lines = flatten_ticket(ticket_dict)
        for t in ticket_lines:
            f_out.write('%s\n' % t)

    f_in.close()
    f_out.close()
    return


if __name__ == '__main__':
    main()
