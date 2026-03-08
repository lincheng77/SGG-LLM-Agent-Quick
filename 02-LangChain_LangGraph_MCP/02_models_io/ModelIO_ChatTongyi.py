#pip install langchain-community
#pip install dashscope
import os
from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage


load_dotenv(encoding='utf-8')
API_KEY = os.getenv("QWEN_API_KEY")
API_URL = os.getenv("QWEN_API_URL")
chatLLM = ChatTongyi(
    api_key=API_KEY,
    model="qwen-plus",
    # streaming=True
)

# 打印结果
print(chatLLM.invoke("你是谁"))

print("*" * 60)

res = chatLLM.stream([HumanMessage(content="你好，你是谁")],
                     # streaming=True
                     )
for r in res:
    print("chat resp:", r.content)