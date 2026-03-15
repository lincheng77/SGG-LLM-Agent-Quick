import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
import os
from langchain_core.runnables import RunnableParallel

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


# 提示词
chat_prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
chat_prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])



# 模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)


# 解析
parser = StrOutputParser ()


# 结果
chain1 = chat_prompt1 | model | parser
chain2 = chat_prompt2 | model | parser

# result= chain1.invoke({"topic": "langchain"})
# logger.info(f"Chain1执行结果:\n {result}")
# logger.info(f"Chain1执行结果类型: {type(result)}")
#
# result= chain2.invoke({"topic": "langchain"})
# logger.info(f"Chain2执行结果:\n {result}")
# logger.info(f"Chain2执行结果类型: {type(result)}")

parallel = RunnableParallel({
    "chain1": chain1,
    "chain2": chain2
})

result = parallel.invoke({"topic": "langchain"})
logger.info(result)

# 打印并行链的ASCII图形表示(LangGraph)
parallel.get_graph().print_ascii()