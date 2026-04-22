from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


def MyOperatorMul(current: float, update: float) -> float:

    if current == 0.0:
        print(f"current:{current}")
        print(f"update:{update}")
        return 1.0 * update
    return current * update

class MultiplyState(TypedDict):
    factor: Annotated[float, MyOperatorMul]


def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}


builder = StateGraph(MultiplyState)

builder.add_node("multiplier", multiplier)

builder.add_edge(START, "multiplier")
builder.add_edge("multiplier", END)

graph = builder.compile()

result = graph.invoke({"factor": 5.0})
print(f"执行结果: {result}")