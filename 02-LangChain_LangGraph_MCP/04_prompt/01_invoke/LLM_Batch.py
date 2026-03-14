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
    "什么是redis?简洁回答，字数控制在100以内",
    "Python的生成器是做什么的？简洁回答，字数控制在100以内",
    "解释一下Docker和Kubernetes的关系?简洁回答，字数控制在100以内"
]

# 3.调用模型
responses = model.batch(messages)
print(f"响应类型：{type(responses)}")


for message, response in zip(messages, responses):
    print(f"问题：{message}\n回答：{response.content}\n")

