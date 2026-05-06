import asyncio

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from langgraph.runtime import Runtime


async def extract_keywords(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("抽取关键词")
    await asyncio.sleep(1)
