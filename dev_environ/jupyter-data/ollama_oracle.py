import json
import requests

class Oracle:

    def __init__(self, url, model):
        self.base_url = url
        self.model = model
        self.context = None

    def query(self, prompt):
        session = requests.Session()
        
        headers = {'Content-Type': 'application/json'}
        url = '%s/api/generate' % self.base_url
        data = {"model": self.model, "prompt": prompt, "stream":False, "context": self.context}

        r = session.post(url, headers=headers, data=json.dumps(data), stream=False)

        output = json.loads(r.content)['response']
        self.context = json.loads(r.content)['context']
        return output

    def query_stream(self, prompt):
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
