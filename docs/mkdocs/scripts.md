# Scripts

## ms_crawler.py

A script for scraping all messages, comments, and reactions from a Microsoft Teams channel and storing this data in JSON format.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/ms_crawler.py](https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/ms_crawler.py).

### Configuration

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

### Command-line arguments

```text
% PYTHONPATH=. python3 scripts/crawlers/ms_crawler.py -h
/Users/amerck/Projects/oms_practicum/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
usage: ms_crawler.py [-h] -c CONFIG

Crawls Microsoft Graph API for Teams messages.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file
```

### Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/ms_crawler.py
```

You will receive the following prompt:

```text
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ABCD12345 to authenticate.
```

Enter the URL in a browser, submit the code, and authenticate to Microsoft as you would normally. Once this is complete, the script should begin downloading data.

### Data structure

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

## find_sn_ticket_numbers.py

A script for pulling a list of ServiceNow ticket numbers from any text file.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/find_sn_ticket_numbers.py](https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/find_sn_ticket_numbers.py).

### Command-line arguments

```text
% python3 find_sn_ticket_numbers.py -h
usage: find_sn_ticket_numbers.py [-h] -i INPUT -o OUTPUT

Find ServiceNow ticket numbers in text file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Text file to search for ServiceNow ticket numbers
  -o OUTPUT, --output OUTPUT
                        Output file to write the found ticket numbers

```

### Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/find_sn_ticket_numbers.py -i ./some_text.json -o ticket_numbers.txt
```


## sn_crawler.py

A script for pulling the contents of ServiceNow tickets from the SN API and stores the data in JSON format.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/sn_crawler.py](https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/sn_crawler.py).

### Configuration

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

### Command-line arguments

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

### Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/sn_crawler.py -c ./config/config.cfg -i ./ticket_numbers.txt -o ticket_output.json
```


## web_crawler.py

A script for crawling a website and copying all HTML and binary files to disk.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/web_crawler.py](https://github.com/amerck/oms_practicum/blob/main/scripts/crawlers/web_crawler.py).

### Initialization

After installing Playwright via pip, run the following command to install browsers:

```shell
playwright install
```

### Configuration

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

### Command-line arguments

```text
% PYTHONPATH=. python3 scripts/crawlers/web_crawler.py -h
usage: web_crawler.py [-h] -c CONFIG

Crawls Microsoft Graph API for Teams messages.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Configuration file
```

### Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/crawlers/web_crawler.py
```


## html_flattener.py

A script for flattening the output of web_crawler.py for embedding.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/data_flattening/html_flattener.py](https://github.com/amerck/oms_practicum/blob/main/scripts/data_flattening/html_flattener.py).

### Command-line arguments

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

### Running

In order to run the script, execute the following command:

```shell
% PYTHONPATH=. python3 scripts/data_flattening/html_flattener.py -d ./html_archive -o flattened_html.md
```


## sn_flattener.py

A script for flattening the output of sn_crawler.py for embedding.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/data_flattening/sn_flattener.py](https://github.com/amerck/oms_practicum/blob/main/scripts/data_flattening/sn_flattener.py).

### Configuration

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

### Command-line arguments

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

### Running

In order to run the script, execute the following command:

```shell
% PYTHONPATH=. python3 scripts/data_flattening/sn_flattener.py -i sn_tickets.json -o sn_output.md -t ./templates
```


## teams_flattener.py

A script for flattening the output of ms_crawler.py for embedding.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/data_flattening/teams_flattener.py](https://github.com/amerck/oms_practicum/blob/main/scripts/data_flattening/teams_flattener.py).

### Configuration

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

### Command-line arguments

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

### Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/data_flattening/teams_flattener.py -i ./message_archive_full.json -o ./flattened_output.md -t ./templates
```


## store_embeddings.py

A script for storing text embeddings in vector database.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/embeddings/store_embeddings.py](https://github.com/amerck/oms_practicum/blob/main/scripts/embeddings/store_embeddings.py).

### Configuration

The script requires a configuration file containing several parameters in the following format:

```text
[vector_db]
host=
port=
collection=

[model]
model_name=
model_size=

[splitter]
chunk_size=
chunk_overlap=
```

* vector_db
    * host: hostname of vector database (**Required**)
    * port: port of vector database (**Required**)
    * collection: collection name for data in vector database (**Required**)
* model
    * model_name: name of the model used for generating embeddings (**Required**)
    * model_size: size of the model (**Required**)
* splitter
    * chunk_size: number of bytes to divide text into for chunking (*Optional*)
    * chunk_overlap: number of bytes to overlap chunks (*Optional*)


### Command-line arguments

```text
% PYTHONPATH=. python3 scripts/embeddings/store_embeddings.py -h
/Users/amerck/Projects/oms_practicum/.venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
  warnings.warn(
usage: store_embeddings.py [-h] -i INPUT -c CONFIG [--json]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the Teams JSON file to store in vector database
  -c CONFIG, --config CONFIG
                        Path to the config file
  --json                Handle input as JSON with metadata.
```

### Running 

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/embeddings/store_embeddings.py -c config/config.cfg -i input_text.json --json
```


## query_vector_db.py

A script for querying a vector database collection for similar text.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/embeddings/query_vector_db.py](https://github.com/amerck/oms_practicum/blob/main/scripts/embeddings/query_vector_db.py).

### Configuration

The script requires a configuration file containing several parameters in the following format:

```text
[vector_db]
host=
port=
collection=

[model]
model_name=
model_size=
```

* vector_db
    * host: hostname of vector database (**Required**)
    * port: port of vector database (**Required**)
    * collection: collection name for data in vector database (**Required**)
* model
    * model_name: name of the model used for generating embeddings (**Required**)
    * model_size: size of the model (**Required**)

### Command-line arguments

```text
% PYTHONPATH=. python3 scripts/embeddings/query_vector_db.py -h
usage: query_vector_db.py [-h] -c CONFIG [prompt]

positional arguments:
  prompt                Query text

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config file
```

### Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/embeddings/query_vector_db.py -c config/config.cfg "What is information security?"
```


## populate_graph_db.py

A script for populating the Graph database with Microsoft Teams alerts and ServiceNow tickets.

This script can be found at [https://github.com/amerck/oms_practicum/blob/main/scripts/graph_db/populate_graph_db.py](https://github.com/amerck/oms_practicum/blob/main/scripts/graph_db/populate_graph_db.py).


## Configuration

The configuration file for `populate_graph_db.py` should use the following structure:

```text
[graph_db]
uri=
username=
password=
```

### Command-line arguments

```text
% PYTHONPATH=. python3 scripts/graph_db/populate_graph_db.py -h
usage: populate_graph_db.py [-h] -c CONFIG --teams TEAMS --sn SN

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config file
  --teams TEAMS         Path to Teams Alert file
  --sn SN               Path to ServiceNow Ticket file
```

### Running

In order to run the script, execute the following command:

```shell
 PYTHONPATH=. python3 scripts/graph_db/populate_graph_db.py -c configs/graph.cfg --teams teams_flattened.json --sn sn_flattened.json
```