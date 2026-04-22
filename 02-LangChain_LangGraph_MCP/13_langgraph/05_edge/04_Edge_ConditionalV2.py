
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated


# 定义状态
class AtguiguState(TypedDict):
    x: int

def addition1(state):
    print(f'加法节点addition1收到的初始值:{state}')
    return {"x": state["x"] + 1}

def addition2(state):
    print(f'加法节点addition2收到的初始值:{state}')
    return {"x": state["x"] + 2}

def addition3(state):
    print(f'加法节点addition3收到的初始值:{state}')
    return {"x": state["x"] + 3}


def route_by_sentiment(state: AtguiguState) -> str:
    # 路由逻辑
    flag = state["x"]
    if flag == 1:
        return "condition_1"
    elif flag == 2:
        return "condition_2"
    else:
        return "condition_3"

graph = StateGraph(AtguiguState)
graph.add_node("node1", addition1)
graph.add_node("node2", addition2)
graph.add_node("node3", addition3)

# 路由边（其实就是多条件）
graph.add_conditional_edges(
    START,
    route_by_sentiment,
    {
        "condition_1": "node1",
        "condition_2": "node2",
        "condition_3": "node3"
    }
)
# 普通边
graph.add_edge("node1", END)
graph.add_edge("node2", END)
graph.add_edge("node3", END)

app = graph.compile()
initial_state ={"x": 3}
result= app.invoke(initial_state)
print(f"最后的结果是:{result}")


print(app.get_graph().print_ascii())