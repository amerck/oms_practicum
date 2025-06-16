import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantDB:

    def __init__(self, host, port, model, size):
        self.client = QdrantClient(host=host, port=port)
        self.model = model
        self.size = size
        self.distance = Distance.COSINE


    def store_vector(self, text, collection_name, metadata=None, progress=False):
        vector = self.model.encode(text)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={'text': text,
                     **metadata}
        )
        self.client.upsert(collection_name=collection_name,
                           points=[point])


    def query_collection(self, query_text, collection_name, limit=5):
        query = self.model.encode(query_text)
        results = self.client.query_points(
            collection_name=collection_name,
            query=query,
            limit=limit
        )
        return results


    def recreate_collection(self, collection_name):
        self.client.delete_collection(collection_name)
        self.client.create_collection(
            collection_name, vectors_config=VectorParams(size=self.size, distance=self.distance)
        )


    def delete_collection(self, collection_name):
        self.client.delete_collection(collection_name)


    def create_collection(self, collection_name):
        self.client.create_collection(
            collection_name, vectors_config=VectorParams(size=self.size, distance=self.distance)
        )
