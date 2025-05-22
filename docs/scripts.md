# Scripts

## ms_crawler.py

This script can be found at [https://github.com/amerck/oms_practicum/tree/main/source/data_scraping/ms_graph](https://github.com/amerck/oms_practicum/tree/main/source/data_scraping/ms_graph).

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

### Running

In order to run the script, execute the following command:

```shell
python3 ms_crawler.py
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

## web_crawler.py

This script can be found at [https://github.com/amerck/oms_practicum/tree/main/source/data_scraping/web_crawler](https://github.com/amerck/oms_practicum/tree/main/source/data_scraping/web_crawler).


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

### Running

In order to run the script, execute the following command:

```shell
python3 web_crawler.py
```