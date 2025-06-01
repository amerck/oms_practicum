from ollama_client import OllamaClient


def main():
    client = OllamaClient("http://localhost:11434", "qwen3:8b")
    client.query_stream("Hello!")
    client.query_stream("Can you tell me a bit more about yourself?")
    client.query_stream("Can you tell me the previous two prompts I sent you?")


if __name__ == '__main__':
    main()
