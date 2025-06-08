# ServiceNow

## find_ticket_numbers.py

Pulls a list of ServiceNow ticket numbers from any text file

### Command-line arguments

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

### Running

In order to run the script, execute the following command:

```shell
python3 find_ticket_numbers.py -i ./some_text.json -o ticket_numbers.txt
```


## sn_crawler.py

Pulls the contents of ServiceNow tickets from the SN API and stores the data in JSON format

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
python3 sn_crawler.py -c ./config/config.cfg -i ./ticket_numbers.txt -o ticket_output.json
```