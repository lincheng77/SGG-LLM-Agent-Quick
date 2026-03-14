# 1.导入依赖
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,SystemMessage
from openai import api_key

load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_URL = os.getenv("QWEN_API_URL")

model = init_chat_model(
    model="qwen3.5-plus",
    model_provider="openai",
    api_key = API_KEY,
    base_url = API_URL
)

# 构建消息列表
messages = [
    SystemMessage(content="你叫小问，是一个乐于助人的AI人工助手"),
    HumanMessage(content="你是谁,你会烦什么")

]

# 3.调用模型
response = model.stream(messages)
print(f"响应类型：{type(response)}")

# 流式打印结果
for chunk in response:
    print(chunk.content, end="", flush=True)

print("\n")

