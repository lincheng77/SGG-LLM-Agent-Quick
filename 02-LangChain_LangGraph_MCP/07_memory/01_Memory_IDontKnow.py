from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from loguru import logger
from langchain_core.runnables import RunnableBranch, RunnableLambda
import os

import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


# 模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)


prompt = PromptTemplate.from_template(
    "请回答我的问题：{question}"
)
parser = StrOutputParser()
chain = prompt | model | parser


print(chain.invoke({"question": "我叫张三，你叫什么?"}))
print("*" * 200)
print(chain.invoke({"question": "你知道我是谁吗?"}))