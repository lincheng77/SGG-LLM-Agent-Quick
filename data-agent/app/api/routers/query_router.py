import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app.api.schemas.query_schema import QuerySchema
from app.clients.embedding_client_manager import embedding_client_manager
from app.clients.es_client_manager import es_client_manager
from app.clients.mysql_client_manager import meta_mysql_client_manager, dw_mysql_client_manager
from app.clients.qdrant_client_manager import qdrant_client_manager
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository
from app.services.query_service import QueryService

query_router = APIRouter()


async def fake_streamer():
    for i in range(10):
        await asyncio.sleep(1)
        yield f"data: step:{i}\n\n"


async def fake_steamer():
    async for chunk in fake_streamer():
        yield chunk


async def get_meta_session():
    async with meta_mysql_client_manager.session_factory() as session:
        yield session

async def get_meta_mysql_repository(session: Annotated[AsyncSession, Depends(get_meta_session)]):
    return MetaMySQLRepository(session)

async def get_dw_session():
    async with dw_mysql_client_manager.session_factory() as session:
        yield session

async def get_dw_mysql_repository(session: Annotated[AsyncSession, Depends(get_dw_session)]):
    return DWMySQLRepository(session)

async def get_column_qdrant_repository():
    return ColumnQdrantRepository(qdrant_client_manager.client)

async def get_metric_qdrant_repository():
    return MetricQdrantRepository(qdrant_client_manager.client)

async def get_embedding_client():
    return embedding_client_manager.client

async def get_value_es_repository():
    return ValueEsRepository(es_client_manager.client)


async def get_query_service(
        meta_mysql_repository: Annotated[MetaMySQLRepository, Depends(get_meta_mysql_repository)],
        dw_mysql_repository: Annotated[DWMySQLRepository, Depends(get_dw_mysql_repository)],

        column_qdrant_repository: Annotated[ColumnQdrantRepository, Depends(get_column_qdrant_repository)],
        metric_qdrant_repository: Annotated[MetricQdrantRepository, Depends(get_metric_qdrant_repository)],
        embedding_client: Annotated[HuggingFaceEndpointEmbeddings, Depends(get_embedding_client)],
        value_es_repository: Annotated[ValueEsRepository, Depends(get_value_es_repository)],
) -> QueryService :
    return QueryService(
        meta_mysql_repository=meta_mysql_repository,
        dw_mysql_repository=dw_mysql_repository,

        column_qdrant_repository=column_qdrant_repository,
        metric_qdrant_repository=metric_qdrant_repository,
        embedding_client=embedding_client,
        value_es_repository=value_es_repository,
    )


@query_router.post("/api/query")
async def query_handler(query: QuerySchema, query_service: QueryService = Depends(get_query_service)):
    return StreamingResponse(query_service.query(query.query), media_type="text/event-stream")
