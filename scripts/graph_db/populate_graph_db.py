import os
import json
import argparse
import configparser
from itso_ai.clients import graph


def store_sn_tickets(sn_ticket_file, client):
    for line in sn_ticket_file.readlines():
        sn_json = json.loads(line)
        if sn_json['metadata']['type'] == 'ticket_body':
            client.store_sn_ticket(sn_json['metadata'])
        elif sn_json['metadata']['type'] == 'work_note':
            client.store_sn_work_note(sn_json['metadata'], sn_json['text'])


def store_teams_alerts(teams_alert_file, client):
    for line in teams_alert_file.readlines():
        teams_json = json.loads(line)
        if teams_json['metadata']['type'] == 'summary':
            client.store_alert_summary(teams_json['metadata'])
        elif teams_json['metadata']['type'] == 'body':
            client.store_teams_body(teams_json['metadata'], teams_json['text'])
        elif teams_json['metadata']['type'] == 'reply':
            client.store_teams_reply(teams_json['metadata'], teams_json['text'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True,
                        help='Path to the config file')
    parser.add_argument('--teams', required=True,
                        help='Path to Teams Alert file')
    parser.add_argument('--sn', required=True,
                        help='Path to ServiceNow Ticket file')
    args = parser.parse_args()

    cfg = configparser.RawConfigParser()
    cfg.read(os.path.expanduser(args.config))
    uri = cfg.get('graph_db', 'uri')
    username = cfg.get('graph_db', 'username')
    password = cfg.get('graph_db', 'password')

    client = graph.GraphDB(uri=uri, username=username, password=password)

    print("Storing ServiceNow Tickets")
    fin = open(os.path.expanduser(args.sn), 'r')
    store_sn_tickets(fin, client)
    fin.close()

    print("Storing Teams Alerts")
    fin = open(os.path.expanduser(args.teams), 'r')
    store_teams_alerts(fin, client)
    fin.close()

    return


if __name__ == "__main__":
    main()
