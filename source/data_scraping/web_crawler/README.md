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
python3 web_crawler.py
```