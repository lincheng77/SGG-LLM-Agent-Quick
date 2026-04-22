from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START,END


class State(TypedDict):
    query: str
    answer: str

def node(state: State):
    writer = get_stream_writer()
    writer({"custom_key": "欢迎来到尚硅谷线上Agent班级学习，O(∩_∩)O"})
    return {"answer": "some data"}


graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .add_edge("node",END)
    .compile()
)

# Set stream_mode="custom" to receive the custom data in the stream
# for chunk in graph.stream({"query": "example"}, stream_mode=["custom"]):
#     print(chunk)
#
for chunk in graph.stream({"query": "example"}, stream_mode=["updates", "custom"]):
    print(chunk)
#
# for chunk in graph.stream({"query": "example"}, stream_mode=["values", "custom"]):
#     print(chunk)
