"""
LangGraph入口点演示

入口点定义了图开始执行的第一个节点。
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# 定义状态
class AtguiguState(TypedDict):
    value: int
    step: str

# 定义节点函数
def node_a(state: AtguiguState) -> dict:
    """节点A"""
    print("执行节点A")
    print("state[value]:"+str(state["value"]))
    print("state[step]:"+str(state["step"]))
    return {"value": state["value"] + 1, "step": "A执行完毕"}


def node_b(state: AtguiguState) -> dict:
    """节点B"""
    print("执行节点B")
    return {"value": state["value"] * 2, "step": "B执行完毕"}

# 创建图
builder = StateGraph(AtguiguState)

# 添加节点
builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)


builder.set_entry_point("node_a")
builder.add_edge("node_a", "node_b")
builder.set_finish_point("node_b")

# 编译图
graph = builder.compile()
# 执行图
result = graph.invoke({"value": 0, "step": "hello"})
print(f"执行结果: {result}\n")
