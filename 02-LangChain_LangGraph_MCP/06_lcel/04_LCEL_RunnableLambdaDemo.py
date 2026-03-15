from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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


# 子链1
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1


# 子链2
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，将用户输入内容翻译成英文"),
    ("human", "{input}")
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2


# 一个简单的打印函数，调试用
def debug_print(x):
    logger.info(f"中间结果:{x}")
    return {"input": x}

# 完整链调用方法1
full_chain = chain1 | debug_print | chain2
result1 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果:{result1}")

#睡眠1分钟
import time
time.sleep(60)
print("#"*100)

# 完整链调用方法2
# 创建一个可运行的调试节点，用于打印中间结果
debug_node = RunnableLambda(debug_print)
full_chain = chain1 | debug_node | chain2
result2 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果:{result2}")