
from typing import TypedDict
from langgraph.graph import StateGraph,START
from langchain.chat_models import init_chat_model
import os

import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


class State(TypedDict):
    query:str
    answer:str


def node(state:State):
    # 模型
    model = init_chat_model(
        model="qwen3.5-flash",
        model_provider="openai",
        api_key=API_KEY,
        base_url=API_RUL
    )

    result = model.invoke( [("user",state["query"])] )
    return {"answer":result}

graph = (
    StateGraph(state_schema=State)
    .add_node(node)
    .add_edge(START,"node")
    .compile()
)

inputs = {"query":"帮我生成一个800字的小学生作文，主题为我的一天"}

for chunk,meta_data in graph.stream(inputs,stream_mode="messages"):
    #print(f"type of chunk:{type(chunk)}")#上课时候打开注释
    print(chunk.content,end="")
    #print(chunk,end="")