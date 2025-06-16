from qdrant_client import QdrantClient
from llama_index.core.tools import FunctionTool
from sentence_transformers import SentenceTransformer


client = QdrantClient(host='localhost', port=6333)


def get_embeddings(text):
    model = SentenceTransformer('all-mpnet-base-v2')
    return model.encode(text)


def teams_vector(query, limit=5):
    print("Teams vector: %s" % query)
    vector = get_embeddings(query)
    print(vector)
    results = client.query_points(
        collection_name='teams_alerts',
        query=vector,
        limit=limit
    )
    print(results)
    return results


def security_site_vector(query, limit=5):
    print("Security site vector: %s" % query)
    vector = get_embeddings(query)
    print(vector)
    results = client.query_points(
        collection_name='itso_site',
        query=vector,
        limit=limit
    )
    print(results)
    return results


def security_wiki_vector(query, limit=5):
    print("Security wiki vector: %s" % query)
    vector = get_embeddings(query)
    print(vector)
    results = client.query_points(
        collection_name='itso_wiki',
        query=vector,
        limit=limit
    )
    print(results)
    return results


teams_vector_tool = FunctionTool.from_defaults(teams_vector,
                                               name='teams vector search',
                                               description='Search teams vectors for IP addresses')

security_site_vector_tool = FunctionTool.from_defaults(security_site_vector,
                                                       name='security site vector search',
                                                       description='Search the security.duke.edu website vectors for relevant information about the prompt.')

security_wiki_vector_tool = FunctionTool.from_defaults(security_wiki_vector,
                                                       name='security wiki vector search',
                                                       description='Search the internal wiki vectors for relevant information about the prompt.')