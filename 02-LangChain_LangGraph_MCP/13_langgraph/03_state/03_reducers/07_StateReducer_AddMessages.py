from typing import Annotated, List

from langchain_core.messages import HumanMessage, AIMessage
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class AddMessagesState(TypedDict):
    messages: Annotated[List, add_messages]

def chat_node_1(state: AddMessagesState) -> dict:
    return {"messages": [("assistant", "Hello from node 1")]}

def chat_node_2(state: AddMessagesState) -> dict:
    return {"messages": [("assistant", "Hello from node 2")]}

# 图
builder = StateGraph(AddMessagesState)

# 节点
builder.add_node("chat1", chat_node_1)
builder.add_node("chat2", chat_node_2)

# 边
builder.add_edge(START, "chat1")
builder.add_edge(START, "chat2")  # 并行执行
builder.add_edge("chat1", END)
builder.add_edge("chat2", END)


graph = builder.compile()
result = graph.invoke({"messages": [("user", "Hi there!")]})
print(f"初始状态: {{'messages': [('user', 'Hi there!')]}}")
print(f"执行结果: {result}\n")

# 打印图的ascii可视化结构
print(graph.get_graph().print_ascii())