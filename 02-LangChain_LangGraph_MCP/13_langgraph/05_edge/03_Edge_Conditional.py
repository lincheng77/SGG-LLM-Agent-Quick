from typing import Optional
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from loguru import logger
from pydantic import BaseModel

"""
LangGraph 条件边
"""


class MyState(BaseModel):
    x: int
    result: Optional[str] = None


# 检查输入状态的节点函数
def check_x(state: MyState) -> MyState:
    logger.info(f"[check_x] Received state: {state}")
    return state


# 判断状态中x值是否为偶数的条件函数
def is_even(state: MyState) -> bool:
    return state.x % 2 == 0


# 处理偶数情况的节点函数
def handle_even(state: MyState) -> MyState:
    logger.info("[handle_even] x 是偶数")
    return MyState(x=state.x, result="even")


# 处理奇数情况的节点函数
def handle_odd(state: MyState) -> MyState:
    logger.info("[handle_odd] x 是奇数")
    return MyState(x=state.x, result="odd")


builder = StateGraph(MyState)
# 添加节点
builder.add_node("check_x", check_x)
builder.add_node("handle_even", handle_even)
builder.add_node("handle_odd", handle_odd)

# 添加起始边
builder.add_edge(START, "check_x")
# 添加条件边
builder.add_conditional_edges("check_x",is_even,
                              {
                                  True: "handle_even",
                                  False: "handle_odd"
                              })
# 添加结束边
builder.add_edge("handle_even", END)
builder.add_edge("handle_odd", END)


graph = builder.compile()
print(graph.get_graph().print_ascii())
logger.info("输入 x=4（偶数）")
graph.invoke(MyState(x=4))

