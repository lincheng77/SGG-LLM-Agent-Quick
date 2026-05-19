from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime

from app.core.log import logger


async def run_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    step = "执行SQL"
    writer({"type": "progress", "step": step, "status": "running"})

    try:
        sql = state["sql"]
        dw_mysql_repository = runtime.context["dw_mysql_repository"]

        result = await dw_mysql_repository.run(sql)

        writer({"type": "progress", "step": step, "status": "success"})
        writer({"type": "result", "data": result})
        logger.info(f"SQL执行结果：{result}")
    except Exception as e:
        logger.error(f"执行SQL失败：{e}")
        writer({"type": "progress", "step": step, "status": "error"})
        raise
