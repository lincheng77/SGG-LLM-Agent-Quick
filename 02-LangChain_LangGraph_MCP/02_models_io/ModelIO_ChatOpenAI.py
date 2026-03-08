from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')
API_KEY = os.getenv("QWEN_API_KEY")

chatLLM = ChatOpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",
    # other params...
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"}]

response = chatLLM.invoke(messages)

print(response.content)