import os
import argparse
import configparser
from sentence_transformers import SentenceTransformer
from itso_ai.clients.vector import QdrantDB


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True,
                        help='Path to the config file')
    parser.add_argument('prompt', nargs='?', help='Query text')
    args = parser.parse_args()

    cfg = configparser.RawConfigParser()
    cfg.read(os.path.expanduser(args.config))

    vector_db_host = cfg.get('vector_db', 'host')
    vector_db_port = cfg.getint('vector_db', 'port')
    collection_name = cfg.get('vector_db', 'collection')
    model_name = cfg.get('model', 'model_name')
    model_size = cfg.get('model', 'model_size')

    model = SentenceTransformer(model_name)
    client = QdrantDB(host=vector_db_host, port=vector_db_port, model=model, size=model_size)
    results = client.query_collection(query_text='How should you disclose a vulnerability?',
                                      collection_name=collection_name)
    print(results)


if __name__ == '__main__':
    main()
