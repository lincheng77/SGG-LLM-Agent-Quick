from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from app.conf.app_config import app_config


class MetricQdrantRepository:
    collection_name = "metric_info_collection"

    def __init__(self, client: AsyncQdrantClient):
        self.client = client

    async def ensure_collection(self):
        if not await self.client.collection_exists(self.collection_name):
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=app_config.qdrant.embedding_size, distance=Distance.COSINE)
            )

    async def upsert(self, ids, embedding, payloads, batch_size: int = 10):
        points: list[PointStruct] = [PointStruct(id=id,
                                                 vector=embedding,
                                                 payload=payload)
                                     for id, embedding, payload in zip(ids, embedding, payloads)]
        for i in range(0, len(points), batch_size):
            await self.client.upsert(collection_name=self.collection_name, points=points[i: i + batch_size])