import asyncio

import yaml
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime

from app.clients.llm import llm
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


async def correct_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("校正SQL")

    table_info_states = state["table_info_states"]
    metric_info_states = state["metric_info_states"]
    date_info = state["date_info"]
    db_info = state["db_info"]
    query = state["query"]
    sql = state["sql"]
    error = state["error"]

    prompt = PromptTemplate(template=load_prompt("correct_sql"),
                            input_variables=["table_info_states", 'metric_info_states',
                                             'date_info', 'db_info', 'query',
                                             'sql', 'error'])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    result = await chain.ainvoke({
        "table_info_states": yaml.dump(table_info_states, allow_unicode=True, sort_keys=False),
        "metric_info_states": yaml.dump(metric_info_states, allow_unicode=True, sort_keys=False),
        "date_info": yaml.dump(date_info, allow_unicode=True, sort_keys=False),
        "db_info": yaml.dump(query, allow_unicode=True, sort_keys=False),
        "query": query,
        "sql": sql,
        "error": error
    })


    logger.info(f"校正后的SQL：{result}")

    return {"sql": result}
