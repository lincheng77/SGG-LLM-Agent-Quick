from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import operator

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]
    tags: Annotated[List[str], operator.add]
    score: Annotated[float, operator.add]

def process_user_message(state: ChatState) -> dict:
    user_message = state["messages"][-1]

    return {
        "messages": [("assistant", f"Echo : {user_message.content}")],
        "tags": ["processed"],
        "score": 1.0
    }

def add_sentiment_tag(state: ChatState)-> dict:
    return {
        "tags": ["positive"],
        "score": 0.5
    }

# 图
builder = StateGraph(ChatState)

builder.add_node("process", process_user_message)
builder.add_node("sentiment", add_sentiment_tag)

builder.add_edge(START, "process")
builder.add_edge(START, "sentiment")
builder.add_edge("process", END)
builder.add_edge("sentiment", END)


graph = builder.compile()

result = graph.invoke({
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "tags": ["greeting"],
    "score": 0.0
})

print(result)