# LangChain1.0+版本使用方式,目前主流,多模型共存


# 1.导入依赖
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()

# 实例化模型
"""
说明：
model="deepseek-chat" 和 base_url="https://api.deepseek.com" 
刚好匹配默认的 model_provider（如 deepseek），因此无需显式传入，函数内部做了智能推导
如果切换成其他模型（如 OpenAI），若默认值不匹配，就需要显式指定 model_provider="openai"。
"""
model = init_chat_model(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API"),
    base_url="https://api.deepseek.com",
)

print(model.invoke("你是谁").content)