# html_flattener.py

## Command-line arguments

```text
% python3 html_flattener.py -h                                                             
usage: html_flattener.py [-h] -d IN_DIRECTORY -o OUTPUT

HTML Archive Flattener

optional arguments:
  -h, --help            show this help message and exit
  -d IN_DIRECTORY, --in-directory IN_DIRECTORY
                        Directory of HTML files to flatten
  -o OUTPUT, --output OUTPUT
                        Output filename
```

## Running

In order to run the script, execute the following command:

```shell
% PYTHONPATH=. python3 scripts/data_flattening/html_flattener.py -d ./html_archive -o flattened_html.md
```


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
% PYTHONPATH=. python3 scripts/data_flattening/sn_flattener.py -i sn_tickets.json -o sn_output.md -t ./templates
```


# teams_flattener.py

## Configuration

The script requires three template files compatible with `string.Template().substitute()`.

* `attachment.template`: Output format for message attachments
* `reply.template`: Output format for message replies
* `message.template`: Output format for flattened Teams messages

Example:
```text
# Teams Message

* Subject: $subject
* Timestamp: $timestamp
* Sender: $sender

## Content
$content
$attachments

## Replies
$replies
```

## Command-line arguments

```text
 % python teams_flattener.py -h                                                                                                     
usage: teams_flattener.py [-h] -i INPUT -o OUTPUT -t TEMPLATE_DIR

Microsoft Teams Message Flattener

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON Teams Message file from ms_crawler.py output
  -o OUTPUT, --output OUTPUT
                        Output filename
  -t TEMPLATE_DIR, --template-dir TEMPLATE_DIR
                        Directory containing output template files
```

## Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/data_flattening/teams_flattener.py -i ./message_archive_full.json -o ./flattened_output.md -t ./templates
```