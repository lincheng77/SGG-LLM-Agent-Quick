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
    SystemMessage(content="你是一个法律助手，只回答法律问题，超出范围的统一回答，非法律问题无可奉告"),
    HumanMessage(content="简单介绍下广告法，一句话告知50字以内")
]

# 3.调用模型
response = model.invoke(messages)
print(f"响应类型：{type(response)}")

print(response.content)
print(response.content_blocks)

