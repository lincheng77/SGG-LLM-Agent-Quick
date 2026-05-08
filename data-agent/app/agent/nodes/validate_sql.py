import asyncio

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime

from app.core.log import logger


async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("校验SQL")

    sql = state["sql"]
    dw_mysql_repository = runtime.context["dw_mysql_repository"]

    try:
        await dw_mysql_repository.validate(sql)
        logger.info("SQL语法正确")
        return {"error": None}
    except Exception as e:
        logger.error(f"SQL语法错误: {str(e)}")
        return {"error": str(e)}
