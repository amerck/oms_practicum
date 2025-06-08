# sn_flattener.py

## Configuration

The script requires one template file compatible with `string.Template().substitute()`.

* `ticket.template`: Output format for ServiceNow tickets

Example:
```text
# ServiceNow Ticket $number

* Created By: $sys_created_by
* Created On: $sys_created_on
* Opened By: $opened_by
* Opened At: $opened_at
* Priority: $priority
* Urgency: $urgency
* Impact: $impact

* Service Offering: $service_offering
* Service Provider: $u_service_provider
* IT Service: $u_it_service
* Application: $u_application

* Assigned To: $assigned_to
* Assignment Group: $assignment_group
* Closed At: $closed_at

## Ticket $number Short Description

$short_description

## Ticket $number Description

$description

## Ticket $number Work Notes

$close_notes
```

## Command-line arguments

```text
% python3 sn_flattener.py -h
usage: sn_flattener.py [-h] -i INPUT -o OUTPUT -t TEMPLATE_DIR

ServiceNow Ticket Flattener

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON ServiceNow Ticket file from sn_crawler.py output
  -o OUTPUT, --output OUTPUT
                        Output filename
  -t TEMPLATE_DIR, --template-dir TEMPLATE_DIR
                        Directory containing output template files
```

## Running

In order to run the script, execute the following command:

```shell
% python3 sn_flattener.py -i sn_tickets.json -o sn_output.md -t ./templates
```