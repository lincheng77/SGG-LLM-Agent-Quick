"""
LangGraph Reducer函数演示 - operator.mul Reducer（数值相乘）
"""

import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
LangGraph默认：0 × 5 × 2 = 0
你想要：1 × 5 × 2 = 10

所以必须：
👉 不要直接用 operator.mul
👉 改用自定义 reducer
"""

class MultiplyState(TypedDict):
    factor: Annotated[float, operator.mul]

def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}

# 图
builder = StateGraph(MultiplyState)

# 节点
builder.add_node("multiplier", multiplier)

# 边
builder.add_edge(START, "multiplier")
builder.add_edge("multiplier", END)

graph = builder.compile()

result = graph.invoke({"factor": 5.0})
print(f"初始状态: {{'factor': 5.0}}")
print(f"执行结果: {result}\n")