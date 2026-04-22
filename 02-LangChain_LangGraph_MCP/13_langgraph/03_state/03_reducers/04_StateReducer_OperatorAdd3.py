"""
LangGraph Reducer函数演示 - 数值累加Reducer
"""


import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class NumberAddState(TypedDict):
    count: Annotated[int, operator.add]



def increment_1(state: NumberAddState) -> dict:
    return {"count": 5}


def increment_2(state: NumberAddState) -> dict:
    return {"count": 3}


builder = StateGraph(NumberAddState)

# 节点
builder.add_node("increment_1", increment_1)
builder.add_node("increment_2", increment_2)

# 执行边
builder.add_edge(START, "increment_1")
builder.add_edge("increment_1", "increment_2")
builder.add_edge("increment_2", END)

graph = builder.compile()

result = graph.invoke({"count": 10})
print(f"初始状态: {{'count': 10}}")
print(f"执行结果: {result}\n")
