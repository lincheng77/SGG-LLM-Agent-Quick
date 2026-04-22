from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
import operator


# 定义状态
class PersistenceDemoState(TypedDict):
    # operator.add：将元素追加到现有元素中，支持列表、字符串、数值类型的追加
    messages: Annotated[list, operator.add]
    step_count: Annotated[int, operator.add]

# 节点函数
def step_one(state: PersistenceDemoState) -> dict:
    print("执行步骤 1")
    return {
        "messages": ["执行了步骤 1"],
        "step_count": 1
    }


def step_two(state: PersistenceDemoState) -> dict:
    print("执行步骤 2")
    return {
        "messages": ["执行了步骤 2"],
        "step_count": 1
    }


def step_three(state: PersistenceDemoState) -> dict:
    print("执行步骤 3")
    return {
        "messages": ["执行了步骤 3"],
        "step_count": 1
    }


# 构建图
def create_graph():
    builder = StateGraph(PersistenceDemoState)

    builder.add_node("step_one", step_one)
    builder.add_node("step_two", step_two)
    builder.add_node("step_three", step_three)

    builder.add_edge(START, "step_one")
    builder.add_edge("step_one", "step_two")
    builder.add_edge("step_two", "step_three")
    builder.add_edge("step_three", END)

    return builder

# 编译图并使用内存存储
graph = create_graph()
app = graph.compile(checkpointer=InMemorySaver())

# 配置线程ID用于存储状态
config = {"configurable": {"thread_id": "user_13811112222"}}
result = app.invoke({"messages": ["开始执行"],"step_count": 0}, config)
print(f"执行结果result: {result}\n")



saved_state = app.get_state(config)
print(f"保存的状态: {saved_state.values}")
print(f"下一个节点: {saved_state.next}\n")


history = app.get_state_history(config)
for checkpoint in history:
    print("=" * 50)
    print(f"当前状态: {checkpoint.values}")


result2 = app.invoke(None, config)
print(f"恢复执行结果: {result2}\n")