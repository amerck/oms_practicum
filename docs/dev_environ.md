# Development Environment

## Running the Development Environment

The development environment can be started by executing the following command from the same directory 
as your `docker-compose.yml` file:

```shell
docker-compose up
```

## Docker Configuration

### [docker-compose.yml](https://github.com/amerck/oms_practicum/tree/main/dev_environ/docker-compose.yml)

```yaml
services:
  jupyter:
    build:
      context: jupyter
    ports:
      - 8889:8888
    volumes:
      - ./jupyter-data:/home/jovyan/work
    command: start-notebook.py --NotebookApp.token='changeme'

  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.18
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ./milvus/etcd:/etcd
    command: etcd -advertise-client-urls=http://etcd:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd
    healthcheck:
      test: [ "CMD", "etcdctl", "endpoint", "health" ]
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    ports:
      - "127.0.0.1:9001:9001"
      - "127.0.0.1:9000:9000"
    volumes:
      - ./milvus/minio:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:9000/minio/health/live" ]
      interval: 30s
      timeout: 20s
      retries: 3

  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.5.12
    command: [ "milvus", "run", "standalone" ]
    security_opt:
      - seccomp:unconfined
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ./milvus/milvus:/var/lib/milvus
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:9091/healthz" ]
      interval: 30s
      start_period: 90s
      timeout: 20s
      retries: 3
    ports:
      - "127.0.0.1:19530:19530"
      - "127.0.0.1:9091:9091"
    depends_on:
      - "etcd"
      - "minio"
```

### [Dockerfile](https://github.com/amerck/oms_practicum/tree/main/dev_environ/jupyter/Dockerfile) 
```dockerfile
FROM quay.io/jupyter/minimal-notebook:latest

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
```


## LLM Platform

* For this project, we're using [Ollama](https://ollama.com/) for testing local LLMs
    * Allows us to keep sensitive security alert data local to machine
    * Installed on base hardware (Macbook Pro with M4 Max CPU)


## Interacting with LLMs

### ollama
```ollama``` commands:

```text
% ollama
Usage:
  ollama [flags]
  ollama [command]

Available Commands:
  serve       Start ollama
  create      Create a model from a Modelfile
  show        Show information for a model
  run         Run a model
  stop        Stop a running model
  pull        Pull a model from a registry
  push        Push a model to a registry
  list        List models
  ps          List running models
  cp          Copy a model
  rm          Remove a model
  help        Help about any command

Flags:
  -h, --help      help for ollama
  -v, --version   Show version information

Use "ollama [command] --help" for more information about a command.
```


### Jupyter Notebooks

[LLM_Chat.ipynb](https://github.com/amerck/oms_practicum/blob/main/dev_environ/jupyter-data/LLM_Chat.ipynb)

```python
import json
import requests

class Oracle:

    def __init__(self, url, model):
        self.base_url = url
        self.model = model
        self.context = None

    def query_model(self, prompt):
        print(self.context)
        session = requests.Session()
        
        headers = {'Content-Type': 'application/json'}
        url = '%s/api/generate' % self.base_url
        data = {"model": self.model, "prompt": prompt, "stream":True, "context": self.context}
        
        r = session.post(url, headers=headers, data=json.dumps(data), stream=True)
        for line in r.iter_lines():
            if line:
                token = json.loads(line)['response']
                print(token, end='')
        self.context = json.loads(line)['context']

        
gemma = Oracle("http://host.docker.internal:11434", "gemma3")
gemma.query_model("Hello! Who are you?")
```


## Vector Database

* For this project, we're using [Milvius](https://milvus.io/)
