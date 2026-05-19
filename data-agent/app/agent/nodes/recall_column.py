from langchain_core import output_parsers
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from rich.prompt import Prompt

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime

from app.clients.llm import llm
from app.core.log import logger
from app.entities.column_info import ColumnInfo
from app.prompt.prompt_loader import load_prompt
from app.repositories.qdrant import column_qdrant_repository


async def recall_column(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "召回字段信息"
    writer({"type": "progress", "step": step, "status": "running"})

    try:
        embedding_client = runtime.context["embedding_client"]
        column_qdrant_repository = runtime.context["column_qdrant_repository"]

        keywords = state["keywords"]
        query = state["query"]


        # 借助LLM扩展关键词
        prompt = PromptTemplate(template=load_prompt("extend_keywords_for_column_recall"), input_variables=["query"])
        output_parser = JsonOutputParser()
        chain = prompt | llm | output_parser

        result = await chain.ainvoke({"query": query})
        keywords = set(keywords + result)

        # 从Qdrant中检索字段信息
        column_info_map: dict[str, ColumnInfo] = {}
        for keyword in keywords:
            # 对keyword 进行Embedding
            embedding = await embedding_client.aembed_query(keyword)
            current_column_infos: list[ColumnInfo] = await column_qdrant_repository.search(embedding)

            for column_info in current_column_infos:
                if column_info.id not in column_info_map: # 要判断一下，因为前面的得分高
                    column_info_map[column_info.id] = column_info
        retrieved_column_infos: list[ColumnInfo] = list(column_info_map.values())

        writer({"type": "progress", "step": step, "status": "success"})
        logger.info(f"检索到字段信息：{list(column_info_map.keys())}")
        return {"retrieved_column_infos": retrieved_column_infos}
    except Exception as e:
        logger.error(f"召回字段信息失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
