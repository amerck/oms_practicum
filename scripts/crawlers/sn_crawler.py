import os
import json
import argparse
import configparser
from itso_ai.clients.servicenow import ServiceNowClient


def main():
    parser = argparse.ArgumentParser(description='SN Crawler')
    parser.add_argument('-c', '--config', required=True,
                        help='ServiceNow API configuration file')
    parser.add_argument('-i', '--input', required=True,
                        help='Input file of ServiceNow tickets to retrieve')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file to write ServiceNow ticket data to')
    args = parser.parse_args()

    cfg = configparser.RawConfigParser()
    cfg.read(os.path.expanduser(args.config))
    sn_url = cfg.get('service_now', 'url')
    sn_username = cfg.get('service_now', 'username')
    sn_password = cfg.get('service_now', 'password')

    client = ServiceNowClient(sn_url, sn_username, sn_password)
    fin = open(args.input, 'r')
    fout = open(args.output, 'w')

    tickets = fin.readlines()
    unique_tickets = list(set(tickets))

    for t in unique_tickets:
        print("Processing ticket %s" % t.strip())
        ticket = client.get_ticket_by_number(t.strip())
        if ticket:
            fout.write('%s\n' % json.dumps(ticket))
        else:
            print("%s not found." % t.strip())

    fin.close()
    fout.close()


if __name__ == "__main__":
    main()
