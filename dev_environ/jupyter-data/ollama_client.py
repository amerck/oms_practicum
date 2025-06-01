import json
import requests


class OllamaClient:

    """
    Client for querying Ollama's API.
    """

    def __init__(self, url, model, think=False):
        """
        Initialize the OllamaClient class

        :param url: base URL of the Ollama API (example: 'http://localhost:11434')
        :param model: the LLM model to use with the client
        :param think: enable thinking for the model
        """
        self.base_url = url
        self.model = model
        self.think = think
        self.context = None     # Maintain chat history across session


    def query(self, prompt):
        """
        Query the Ollama API without streaming.

        :param prompt: The prompt to be sent to the Ollama API
        :return: Ollama response
        """
        session = requests.Session()

        headers = {'Content-Type': 'application/json'}
        url = '%s/api/generate' % self.base_url
        data = {"model": self.model, "prompt": prompt, "stream": False, "context": self.context, "think": self.think}

        r = session.post(url, headers=headers, data=json.dumps(data), stream=False)

        output = json.loads(r.content)['response']
        self.context = json.loads(r.content)['context']     # Update the context to maintain history
        return output


    def query_stream(self, prompt):
        """
        Query the Ollama API with streaming, and print output in real time.

        :param prompt: The prompt to be sent to the Ollama API
        :return: None
        """
        print(self.context)
        session = requests.Session()

        headers = {'Content-Type': 'application/json'}
        url = '%s/api/generate' % self.base_url
        data = {"model": self.model, "prompt": prompt, "stream": True, "context": self.context, "think": self.think}

        r = session.post(url, headers=headers, data=json.dumps(data), stream=True)
        for line in r.iter_lines():
            if line:
                line_json = json.loads(line)
                token = line_json['response']
                print(token, end='')

                if 'context' in line_json.keys():
                    self.context = line_json['context'] # Update the context to maintain history
