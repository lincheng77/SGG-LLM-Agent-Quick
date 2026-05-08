import asyncio
from idlelib import query

import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, TableInfoState
from langgraph.runtime import Runtime

from app.clients.llm import llm
from app.core.log import logger
from app.entities import column_info
from app.prompt.prompt_loader import load_prompt


async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer

    query = state["query"]
    table_info_states = state["table_info_states"]

    # 借助LLM扩展关键词
    prompt = PromptTemplate(template=load_prompt("filter_table_info"), input_variables=["query", 'table_info_states'])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser

    reslut = await chain.ainvoke({
        "query": query,
        "table_info_states": yaml.dump(
            table_info_states,
            allow_unicode=True,  # 保留中文字符，避免转义成 \uXXXX
            sort_keys=False)
    })

    # print(yaml.dump(table_info_states, allow_unicode=True, sort_keys= False))

    filtered_table_info_states: list[TableInfoState] = []
    # 过滤得到符合的表
    for table_info_state in table_info_states:
        if table_info_state['name'] in reslut:
            filtered_table_info_states.append(table_info_state)
            # 过滤得到符合的字段
            table_info_state['columns'] = [column_info_state for column_info_state in table_info_state['columns'] if
                                           column_info_state['name'] in reslut[table_info_state['name']]]

    logger.info(f"过滤后的表信息：{[filtered_table_info_state['name'] for filtered_table_info_state in filtered_table_info_states]}")
    return {"table_info_states": filtered_table_info_states}