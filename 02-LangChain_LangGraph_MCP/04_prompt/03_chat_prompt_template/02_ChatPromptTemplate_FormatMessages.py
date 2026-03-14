import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import dotenv

dotenv.load_dotenv(encoding="utf-8")

# 提示词模板
chatPrompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}。"),
        ("human", "你能帮我做什么?"),
        ("ai", "我能开发很多{thing}。"),
        ("human", "{user_input}"),
    ]
)

prompt = chatPrompt.format_messages(
    name="小谷AI", thing="AI", user_input="7 + 5等于多少")
print(prompt)


# 模型
API_KEY = os.getenv("QWEN_API_KEY")
API_URL = os.getenv("QWEN_API_URL")
model = init_chat_model(
    model="qwen-flash-character-2026-02-26",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_URL,
)

# 调用
result = model.invoke(prompt)
print(result.content)
print("\n\n")
