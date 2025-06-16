# ms_crawler.py

## Configuration

The configuration file for `ms_crawler.py` should be stored under `./config/config.cfg` with the following structure:

```text
[azure]
clientId = 
tenantId = 
graphUserScopes = User.Read Team.ReadBasic.All

[teams]
teamId = 
channelId = 
outputFile = output/message_archive.json
```

## Running

In order to run the script, execute the following command:

```shell
python3 ms_crawler.py
```

You will receive the following prompt:

```text
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ABCD12345 to authenticate.
```

Enter the URL in a browser, submit the code, and authenticate to Microsoft as you would normally. Once this is complete, the script should begin downloading data.

## Data structure

```json
{
  "message": {
    "attachments": [
      {
        "id": "Unique identifier for attachment",
        "content": "Attachment body text"
        "content_type": "Attachment data type",
      }
    ],
    "content_type": "Teams message data type",
    "content": "Teams message body text",
    "timestamp": "Message creation date and time in TZ format",
    "user": "Message author",
    "reactions": [
      {
        "reaction_name": "Name of emoji reaction",
        "reaction_type": "Reaction emoji",
        "timestamp": "Timestamp of reaction"
      }
    ],
    "replies": [
      {
        "content": "Reply body text",
        "content_type": "Reply data type",
        "timestamp": "Timestamp of reply",
        "user": "Reply author",
        "reactions": [
          {
            "reaction_name": "Name of emoji reaction",
            "reaction_type": "Reaction emoji",
            "timestamp": "Timestamp of reaction"
          }
        ]
      }
    ]
  }
}
```

# find_ticket_numbers.py

Pulls a list of ServiceNow ticket numbers from any text file

## Command-line arguments

```text
% python3 find_ticket_numbers.py -h
usage: find_ticket_numbers.py [-h] -i INPUT -o OUTPUT

Find ServiceNow ticket numbers in text file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Text file to search for ServiceNow ticket numbers
  -o OUTPUT, --output OUTPUT
                        Output file to write the found ticket numbers

```

## Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/find_ticket_numbers.py -i ./some_text.json -o ticket_numbers.txt
```


# sn_crawler.py

Pulls the contents of ServiceNow tickets from the SN API and stores the data in JSON format

## Configuration

The script requires a configuration file containing ServiceNow authentication parameters in the following format:

```text
[service_now]
url=
username=
password=
```

* **url**: full base URL of ServiceNow instance
* **username**: Username of user with permissions to the ServiceNow API
* **password**: Password for user with permissions to the ServiceNow API

## Command-line arguments

```text
% python3 sn_crawler.py -h         
usage: sn_crawler.py [-h] -c CONFIG -i INPUT -o OUTPUT

SN Crawler

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        ServiceNow API configuration file
  -i INPUT, --input INPUT
                        Input file of ServiceNow tickets to retrieve
  -o OUTPUT, --output OUTPUT
                        Output file to write ServiceNow ticket data to

```

## Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/sn_crawler.py -c ./config/config.cfg -i ./ticket_numbers.txt -o ticket_output.json
```


# web_crawler.py

## Initialization

After installing Playwright via pip, run the following command to install browsers:

```shell
playwright install
```

## Configuration

The configuration file for `web_crawler.py` should be stored under `./config/config.cfg` with the following structure:

```text
[crawler]
domain = 
auth_url = 
auth_verification_url = 
state_path = ./state.json
output_dir = ./archive
```

Description of the configuration options are as follows:
* domain: The base domain name of the site you wish to crawl
* auth_url: The URL to authenticate against prior to scanning
* auth_verification_url: The URL that confirms authentication was successful
* state_path: The path for the Playwright state file
* output_dir: The path of the directory to write the HTML archive to

## Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/web_crawler.py
```