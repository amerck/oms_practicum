# populate_graph_db.py

Populate the Graph database with Microsoft Teams alerts and ServiceNow tickets.

## Configuration

The configuration file for `populate_graph_db.py` should use the following structure:

```text
[graph_db]
uri=
username=
password=
```

## Command-line arguments

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

## Running

In order to run the script, execute the following command:

```shell
 PYTHONPATH=. python3 scripts/graph_db/populate_graph_db.py -c configs/graph.cfg --teams teams_flattened.json --sn sn_flattened.json
```