# store_embeddings.py

A script for storing text embeddings in vector database.

## Configuration

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


## Command-line arguments

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

## Running 

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/embeddings/store_embeddings.py -c config/config.cfg -i input_text.json --json
```


# query_vector_db.py

A script for querying a vector database collection for similar text.

## Configuration

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

## Command-line arguments

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

## Running

In order to run the script, execute the following command:

```shell
PYTHONPATH=. python3 scripts/embeddings/query_vector_db.py -c config/config.cfg "What is information security?"
```
