from langgraph.constants import START, END
from langgraph.graph import StateGraph


def addition(state):
    print(f'加法节点收到的初始值:{state}')
    return {"x": state["x"] + 1}

def subtraction(state):
    print(f'减法节点收到的初始值:{state}')
    return {"x": state["x"] - 2}


graph = StateGraph(dict)


graph.add_node("addition", addition)
graph.add_node("subtraction", subtraction)


graph.add_edge(START, "addition")
graph.add_edge("addition", "subtraction")
graph.add_edge("subtraction", END)

# 打印图的边和节点信息
print(graph.edges)
print()
print(graph.nodes)


app = graph.compile()
initial_state={"x": 5}
result= app.invoke(initial_state)
print(f"最后的结果是:{result}")


print(app.get_graph().print_ascii())
print(app.get_graph().draw_mermaid())