import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import dotenv

dotenv.load_dotenv(encoding="utf-8")

# 提示词模板
template = PromptTemplate(
    template="你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}",
    input_variables=["role", "question"]
)
prompt = template.format_prompt(role="python开发", question="冒泡排序怎么写,只要代码其它不要，简洁")
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
