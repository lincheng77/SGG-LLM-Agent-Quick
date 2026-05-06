import asyncio

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime


async def add_extra_context(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("添加额外上下文")
    await asyncio.sleep(1)
