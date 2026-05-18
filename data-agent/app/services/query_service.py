import json
from collections.abc import AsyncIterator

from fastapi import Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.agent.context import DataAgentContext
from app.agent.graph import graph
from app.agent.state import DataAgentState
from app.api.schemas.query_schema import QuerySchema
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import dw_mysql_client_manager, meta_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository


class QueryService:

    def __init__(self, dw_mysql_repository: DWMySQLRepository = Depends(DWMySQLRepository),
                 meta_mysql_repository: MetaMySQLRepository = Depends(MetaMySQLRepository),
                 column_qdrant_repository: ColumnQdrantRepository = Depends(ColumnQdrantRepository),
                 metric_qdrant_repository: MetricQdrantRepository = Depends(MetricQdrantRepository),
                 embedding_client: HuggingFaceEndpointEmbeddings = Depends(embedding_client_manager),
                 value_es_repository: ValueEsRepository = Depends(ValueEsRepository)):
        self.meta_mysql_repository = meta_mysql_repository
        self.dw_mysql_repository = dw_mysql_repository
        self.column_qdrant_repository = column_qdrant_repository
        self.metric_qdrant_repository = metric_qdrant_repository
        self.embedding_client = embedding_client
        self.value_es_repository = value_es_repository

    async def query(self, query: str):
        state = DataAgentState(query=query)
        context = DataAgentContext(column_qdrant_repository=self.column_qdrant_repository,
                                   metric_qdrant_repository=self.metric_qdrant_repository,
                                   embedding_client=self.embedding_client,
                                   value_es_repository=self.value_es_repository,
                                   meta_mysql_repository=self.meta_mysql_repository,
                                   dw_mysql_repository=self.dw_mysql_repository)

        try:
            async for chunk in graph.astream(input=state, context=context, stream_mode="custom"):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"
