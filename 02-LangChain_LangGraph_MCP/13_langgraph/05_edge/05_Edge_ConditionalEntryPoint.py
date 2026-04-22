from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义简单的状态
class SimpleState(TypedDict):
    user_input: str
    response: str
    node_visited: str


# 2. 路由函数
def route_input(state: SimpleState) -> str:
    text = state["user_input"].lower()

    if "hello" in text or "hi" in text:
        return "greeting"  # 返回路由键
    elif "bye" in text or "exit" in text:
        return "farewell"  # 返回路由键
    else:
        return "question"  # 返回路由键


# 3. 各个处理节点
def handle_greeting(state: SimpleState) -> SimpleState:
    """处理问候"""
    state["response"] = "你好！很高兴见到你！"
    state["node_visited"] = "greeting_node"
    return state


def handle_farewell(state: SimpleState) -> SimpleState:
    """处理告别"""
    state["response"] = "再见！祝你有个美好的一天！"
    state["node_visited"] = "farewell_node"
    return state


def handle_question(state: SimpleState) -> SimpleState:
    """处理问题"""
    state["response"] = "我听到了你的问题，需要更多帮助吗？"
    state["node_visited"] = "question_node"
    return state

# 4. 创建图
def create_simple_graph():

    stateGraph = StateGraph(SimpleState)

    # 添加节点
    stateGraph.add_node("greeting_node", handle_greeting)
    stateGraph.add_node("farewell_node", handle_farewell)
    stateGraph.add_node("question_node", handle_question)

    # 添加路由边（多条件边）
    stateGraph.add_conditional_edges(
        START,
        route_input,
        {
            "greeting": "greeting_node",
            "farewell": "farewell_node",
            "question": "question_node"
        }
    )

    # 所有节点都到END
    stateGraph.add_edge("greeting_node", END)
    stateGraph.add_edge("farewell_node", END)
    stateGraph.add_edge("question_node", END)

    return stateGraph.compile()


if __name__ == '__main__':
    graph = create_simple_graph()

    # 测试不同的输入
    test_inputs = [
        "Hello everyone!",
        "Goodbye now",
        "What time is it?"
    ]

    for user_input in test_inputs:
        print(f"\n输入: {user_input}")


        # 创建初始状态
        initial_state = SimpleState(
            user_input=user_input,
            response="",
            node_visited=""
        )

        # 执行图
        result = graph.invoke(initial_state)

        print(f"路由决策: {route_input(initial_state)}")
        print(f"访问的节点: {result['node_visited']}")
        print(f"响应: {result['response']}")
        print("-" * 30)