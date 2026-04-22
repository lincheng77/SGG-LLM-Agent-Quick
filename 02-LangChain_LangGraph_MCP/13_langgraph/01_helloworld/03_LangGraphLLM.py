import uuid
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")
REDIS_URL = os.getenv("REDIS_URL")



#  1. 定义状态（State）
class LinCheng(TypedDict):
    # messages 是一个消息列表，Annotated + add_messages 表示支持自动追加消息
    messages: Annotated[List, add_messages]



#  2. 定义大模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)


# 3. 定义节点函数
def model_node(state: LinCheng):
    reply = model.invoke(state["messages"])   # 输入历史消息，调用模型
    return {"messages": [reply]}            # 返回新消息，自动加到 state

# 4. 构建图结构
graph = StateGraph(LinCheng)

graph.add_node("model", model_node)

graph.add_edge(START, "model")
graph.add_edge("model", END)

# 5. 编译
app = graph.compile()

# 6. 运行
result = app.invoke({"messages": "请用一句话解释什么是 LangGraph。"})
print("模型回答：", result["messages"][-1].content)


