from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')
API_KEY = os.getenv("DEEPSEEK_API")
API_URL = os.getenv("DEEPSEEK_URL")


model = ChatDeepSeek(
    api_key=API_KEY,
    base_url=API_URL,
    model="deepseek-chat",

    max_tokens=None,
    timeout=None,
    max_retries=2,
)



print(model.invoke("什么是LangChain?100字以内回答，简洁"))