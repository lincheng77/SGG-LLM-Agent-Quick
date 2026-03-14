import os

from datetime import datetime
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import dotenv

dotenv.load_dotenv(encoding="utf-8")


# 模板1
template = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n") + "内容不超过{length}个字"
prompt = template.format(topic="LangChain", length=100)
print(prompt)


# 模板2（合并）
template_a = PromptTemplate.from_template("请用一句话介绍{topic}，要求通俗易懂\n")
template_b = PromptTemplate.from_template("内容不超过{length}个字")
template= template_a + template_b
prompt = template.format(topic="LangChain", length=200)
print(prompt)


# 模型
API_KEY = os.getenv("QWEN_API_KEY")
API_URL = os.getenv("QWEN_API_URL")
model = init_chat_model(
    model="qwen3.5-plus",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_URL,
)

# 调用
result = model.invoke(prompt)
print(result.content)
print("\n\n")
