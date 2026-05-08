import asyncio

import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime

from app.clients.llm import llm
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


async def filter_metric(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer

    query = state["query"]
    metric_info_states = state["metric_info_states"]

    # 借助LLM扩展关键词
    prompt = PromptTemplate(template=load_prompt("filter_metric_info"), input_variables=["query", 'metric_info_states'])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser

    reslut = await chain.ainvoke({
        "query": query,
        "metric_info_states": yaml.dump(
            metric_info_states,
            allow_unicode=True,  # 保留中文字符，避免转义成 \uXXXX
            sort_keys=False)
    })

    filtered_metric_info_states = [metric_info_state for metric_info_state in metric_info_states if
                                   metric_info_state['name'] in reslut]

    logger.info(
        f"过滤后的指标信息：{[filtered_table_info_state['name'] for filtered_table_info_state in filtered_metric_info_states]}")
    return {"metric_info_states": filtered_metric_info_states}
