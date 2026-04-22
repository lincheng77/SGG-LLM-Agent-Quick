import os
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


# 模型
model = init_chat_model(
    model="qwen3.5-flash",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)

checkpointer = InMemorySaver()
agent = create_agent(model=model,checkpointer=checkpointer)


config = {"configurable": {"thread_id": "user-001"}}

msg1 = agent.invoke({"messages": [("user", "你好，我叫张三，喜欢足球，60字内简洁回复")]}, config)
print(msg1["messages"][-1])
msg1["messages"][-1].pretty_print()

msg2 = agent.invoke({"messages": [("user", "我叫什么？我喜欢做什么？")]}, config)
msg2["messages"][-1].pretty_print()