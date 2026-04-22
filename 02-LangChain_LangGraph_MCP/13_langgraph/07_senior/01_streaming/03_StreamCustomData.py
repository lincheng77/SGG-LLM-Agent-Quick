from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END



class State(TypedDict):
    query: str
    answer: str
    progress: list


def node_with_custom_streaming(state: State) -> State:

    writer = get_stream_writer()

    # 发送自定义数据（例如，进度更新）
    writer({"custom_key": "开始处理查询"})
    writer({"progress": "步骤1: 分析查询内容", "status": "running"})

    query = state["query"]

    writer({"progress": "步骤2: 生成结果", "status": "running"})
    writer({"progress": "步骤3: 完成处理", "status": "completed"})
    writer({"custom_key": "查询处理完成"})

    # 模拟处理过程
    result = f"处理结果: {query.upper()}"
    return {
        "answer": result,
        "progress": state.get("progress", []) + ["处理完成"]
    }


# 构建图
graph = (
    StateGraph(State)
    .add_node("node_with_custom_streaming", node_with_custom_streaming)
    .add_edge(START, "node_with_custom_streaming")
    .add_edge("node_with_custom_streaming", END)
    .compile()
)

inputs = {"query": "hello world", "answer": "", "progress": []}


# print("--- 1. 单独使用 custom 流模式 ---")
# for chunk in graph.stream(inputs, stream_mode="custom"):
#     print(f"自定义数据块: {chunk}")


# print("--- 2. 单独使用 updates 流模式 ---")
# for chunk in graph.stream(inputs, stream_mode="updates"):
#     print(f"状态更新: {chunk}")

print("--- 3. 同时使用 custom 和 updates 流模式 ---")
for mode, chunk in graph.stream(inputs, stream_mode=["custom", "updates"]):
    print(f"[{mode}]: {chunk}")