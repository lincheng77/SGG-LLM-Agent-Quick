import uuid
from dataclasses import asdict
from pathlib import Path

from langchain_huggingface import HuggingFaceEndpointEmbeddings
from omegaconf import OmegaConf
from app.conf.meta_config import MetaConfig
from app.entities.column_info import ColumnInfo
from app.entities.table_info import TableInfo
from app.models import column_info
from app.models.column_info import ColumnInfoMySQL
from app.models.table_info import TableInfoMySQL
from app.repositories.es.value_es_repository import ValueEsRepository
from app.repositories.mysql.dw.dw_mysql_repository import DWMySQLRepository
from app.repositories.mysql.meta.meta_mysql_repository import MetaMySQLRepository

from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository


class MetaKnowledgeService:

    def __init__(self,
                 meta_mysql_repository: MetaMySQLRepository,
                 dw_mysql_repository: DWMySQLRepository,
                 column_qdrant_repository: ColumnQdrantRepository,
                 embedding_client: HuggingFaceEndpointEmbeddings,
                 value_es_repository: ValueEsRepository):
        self.meta_mysql_repository: MetaMySQLRepository = meta_mysql_repository
        self.dw_mysql_repository: DWMySQLRepository = dw_mysql_repository
        self.column_qdrant_repository: ColumnQdrantRepository = column_qdrant_repository
        self.embedding_client: HuggingFaceEndpointEmbeddings = embedding_client
        self.value_es_repository: ValueEsRepository = value_es_repository
    



    async def build(self, config_path: Path):
        # 1. 读取配置文件

        context = OmegaConf.load(config_path)
        schema = OmegaConf.structured(MetaConfig)
        meta_config: MetaConfig = OmegaConf.to_object(OmegaConf.merge(schema, context))


        # 2.根据配置文件同步指定的表信息
        if meta_config.tables:
            # 2.1 将表信息和字段信息保存到meta数据库中
            column_infos = await self._save_tables_to_meta_db(meta_config)
            
            # 2.2 对字段信息建立向量索引
            await self._save_columns_to_qdrant(column_infos)

            # 2.3 对指定维度字段值建立全文索引
            await self._save_values_to_es(meta_config)

        # 3.处理指标信息
        if meta_config.metrics:
            # 3.1 将指标信息保存到meta数据库中
            for metric in meta_config.metrics:
                pass
            # 3.2 将指标信息建立向量索引



    async def _save_tables_to_meta_db(self, meta_config: MetaConfig) -> list[ColumnInfo]:
        table_infos: list[TableInfo] = []
        column_infos: list[ColumnInfo] = []
        for table in meta_config.tables:
            # 2.1.1 保存表信息
            table_info = TableInfo(id=table.name,
                                   name=table.name,
                                   description=table.description)
            table_infos.append(table_info)

            # 2.1.2 保存字段信息
            # 查询字段类型
            column_types = await self.dw_mysql_repository.get_column_type(table.name)
            for column in table.columns:
                # 查询字段取值示例
                column_examples = await  self.dw_mysql_repository.get_column_examples(table.name, column.name)
                column_info = ColumnInfo(id=f"{table.name}.{column.name}",
                                         name=column.name,
                                         type=column_types[column.name],
                                         role=column.role,
                                         examples=column_examples,
                                         description=column.description,
                                         alias=column.alias,
                                         table_id=table.name)
                column_infos.append(column_info)
        async with self.meta_mysql_repository.session.begin():
            self.meta_mysql_repository.save_table_infos(table_infos)
            self.meta_mysql_repository.save_column_infos(column_infos)
            
        return column_infos
    
    

    async def _save_columns_to_qdrant(self, column_infos: list[ColumnInfo]):
        await self.column_qdrant_repository.ensure_collection()

        points: list[dict] = []
        for column_info in column_infos:
            points.append(
                {
                    "id": uuid.uuid4(),
                    "embedding_text": column_info.name,
                    "payload": asdict(column_info)
                }
            )

            points.append(
                {
                    "id": uuid.uuid4(),
                    "embedding_text": column_info.description,
                    "payload": asdict(column_info)
                }
            )

            for alia in column_info.alias:
                points.append(
                    {
                        "id": uuid.uuid4(),
                        "embedding_text": alia,
                        "payload": asdict(column_info)
                    }
                )

        # 向量化
        embedding: list[list[float]] = []
        embedding_texts = [point["embedding_text"] for point in points]
        embedding_batch_size = 20
        for i in range(0, len(embedding_texts), embedding_batch_size):
            batch_embedding_texts = embedding_texts[i:i+embedding_batch_size]
            batch_embeddings = await self.embedding_client.aembed_documents(batch_embedding_texts)
            embedding.extend(batch_embeddings)

        ids = [point["id"] for point in points]
        payloads = [point["payload"] for point in points]
        await self.column_qdrant_repository.upsert(ids, embedding, payloads)

    async def _save_values_to_es(self, meta_config):
        await self.value_es_repository.ensure_index()