# Project Training Tests and Development Environment

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
    command: start-notebook.py
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
* ```ollama``` command

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


## Sentence Transformers

* This project will be using SBERT Pretrained Models for Sentence Transformers, found here: [https://www.sbert.net/docs/sentence_transformer/pretrained_models.html](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
* Potential models:
    * all-mpnet-base-v2: "All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs."
    * multi-qa-mpnet-base-dot-v1: "This model was tuned for semantic search: Given a query/question, it can find relevant passages. It was trained on a large and diverse set of (question, answer) pairs."
    * all-distilroberta-v1: "All-round model tuned for many use-cases. Trained on a large and diverse dataset of over 1 billion training pairs."
    * multi-qa-distilbert-cos-v1: "This model was tuned for semantic search: Given a query/question, it can find relevant passages. It was trained on a large and diverse set of (question, answer) pairs."