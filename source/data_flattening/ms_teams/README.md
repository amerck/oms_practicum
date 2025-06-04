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
python teams_flattener.py -i ./message_archive_full.json -o ./flattened_output.md -t ./templates
```
