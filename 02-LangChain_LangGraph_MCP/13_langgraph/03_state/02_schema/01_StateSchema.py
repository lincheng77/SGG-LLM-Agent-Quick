
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

"""
LangGraph 图输入输出模式和私有状态传递演示

该演示展示了：
1. 如何定义图的输入和输出模式
"""

# 定义输入状态模式
class InputState(TypedDict):
    question: str

# 定义输出状态模式
class OutputState(TypedDict):
    answer: str


# 定义整体状态模式，结合输入和输出
class OverallState(InputState, OutputState):
    pass

# 定义处理节点
def answer_node(state: InputState):

    print(f"执行 answer_node 节点:")
    print(f"  输入: {state}")

    # 示例答案
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}

    print(f"  输出: {result}")
    return result


# 使用指定的输入和输出模式构建图
graph = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

graph.add_node("answer_node", answer_node)  # 添加答案节点

graph.add_edge(START, "answer_node")  # 定义起始边
graph.add_edge("answer_node", END)  # 定义结束边

app = graph.compile()  # 编译图


result = app.invoke({"question": "你好"})
print(f"结果: {result}")