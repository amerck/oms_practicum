import os
import json
import argparse
import configparser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from itso_ai.clients.vector import QdrantDB


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help='Path to the Teams JSON file to store in vector database')
    parser.add_argument('-c', '--config', required=True,
                        help='Path to the config file')
    parser.add_argument('--json', required=False, action='store_true',
                        help='Handle input as JSON with metadata.')
    args = parser.parse_args()

    cfg = configparser.RawConfigParser()
    cfg.read(os.path.expanduser(args.config))

    vector_db_host = cfg.get('vector_db', 'host')
    vector_db_port = cfg.getint('vector_db', 'port')
    collection_name = cfg.get('vector_db', 'collection')
    model_name = cfg.get('model', 'model_name')
    model_size = cfg.get('model', 'model_size')

    fin = open(args.input, 'r')

    if cfg.has_section('splitter'):
        chunk_size = cfg.getint('splitter', 'chunk_size')
        chunk_overlap = cfg.getint('splitter', 'chunk_overlap')
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = splitter.split_text(fin.read())
    else:
        chunks = fin.readlines()

    model = SentenceTransformer(model_name)
    client = QdrantDB(host=vector_db_host, port=vector_db_port, model=model, size=model_size)
    client.recreate_collection(collection_name)

    for i, chunk in enumerate(chunks):
        if i % 1000 == 0:
            print("Processing chunk {}/{}".format(i, len(chunks)))
        if args.json:
            text_dict = json.loads(chunk)
            text = text_dict.get('text')
            metadata = text_dict.get('metadata')
            client.store_vector(text=text, collection_name=collection_name, metadata=metadata, progress=True)
        else:
            client.store_vector(text=chunk, collection_name=collection_name, progress=True)

    fin.close()
    return


if __name__ == '__main__':
    main()
