import os
import json
import argparse
import configparser
import pysnc


def process_task(gr):
    task_dict = {'u_service_provider': gr.u_service_provider.get_display_value(),
                 'sys_updated_on': gr.sys_updated_on.get_display_value(),
                 'number': gr.number.get_display_value(),
                 'opened_by': gr.opened_by.get_display_value(),
                 'sys_created_on': gr.sys_created_on.get_display_value(),
                 'sys_created_by': gr.sys_created_by.get_display_value(),
                 'closed_at': gr.closed_at.get_display_value(),
                 'impact': gr.impact.get_display_value(),
                 'priority': gr.priority.get_display_value(),
                 'u_it_service': gr.u_it_service.get_display_value(),
                 'opened_at': gr.opened_at.get_display_value(),
                 'short_description': gr.short_description.get_display_value(),
                 'assignment_group': gr.assignment_group.get_display_value(),
                 'description': gr.description.get_display_value(),
                 'close_notes': gr.close_notes.get_display_value(),
                 'service_offering': gr.service_offering.get_display_value(),
                 'sys_id': gr.sys_id.get_display_value(),
                 'urgency': gr.urgency.get_display_value(),
                 'assigned_to': gr.assigned_to.get_display_value(),
                 'u_application': gr.u_application.get_display_value()}
    return {'ticket': task_dict}


def handle_task(task_number, client):
    gr = client.GlideRecord('task')
    gr.get('number', task_number)
    if not gr:
        return None
    task = process_task(gr)
    return task


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

    client = pysnc.ServiceNowClient(sn_url, (sn_username, sn_password))
    fin = open(args.input, 'r')
    fout = open(args.output, 'w')

    for line in fin:
        task = handle_task(line.strip(), client)
        if task:
            fout.write('%s\n' % json.dumps(task))
        else:
            print("%s not found." % line.strip())

    fin.close()
    fout.close()


if __name__ == "__main__":
    main()
