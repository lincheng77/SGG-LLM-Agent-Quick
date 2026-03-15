from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
from langchain_core.runnables import RunnableBranch
import os

import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


# 提示词
english_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个英语翻译专家，你叫小英"),
    ("human", "{query}")
])

japanese_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个日语翻译专家，你叫小日"),
    ("human", "{query}")
])

korean_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个韩语翻译专家，你叫小韩"),
    ("human", "{query}")
])
def determine_language(inputs):
    """判断语言种类"""
    query = inputs["query"]
    if "日语" in query:
        return "japanese"
    elif "韩语" in query:
        return "korean"
    else:
        return "english"


# 模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)

# 解析
parser = StrOutputParser()


chain = RunnableBranch(
    (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
    (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
    english_prompt | model | parser
)

test_queries = [
    {'query': '请你用韩语翻译这句话:"见到你很高兴"'},
    {'query': '请你用日语翻译这句话:"见到你很高兴"'},
    {'query': '请你用英语翻译这句话:"见到你很高兴"'}
]


for query_input in test_queries:

    """
        下面注释掉的代码，是打印用的，不打印也不影响整体流程！
    
        # # 判断使用哪个提示词
        # lang = determine_language(query_input)
        # logger.info(f"检测到语言类型: {lang}")
        #
        # # 根据语言类型选择对应的提示词并格式化
        # if lang == "japanese":
        #     chatPromptTemplate = japanese_prompt
        # elif lang == "korean":
        #     chatPromptTemplate = korean_prompt
        # else:
        #     chatPromptTemplate = english_prompt
        #
        #
        # # 格式化提示词并打印
        # formatted_messages = chatPromptTemplate.format_messages(**query_input)
        # logger.info("格式化后的提示词:")
        # for msg in formatted_messages:
        #     logger.info(f"[{msg.type}]: {msg.content}")
    """


    # 执行链
    result = chain.invoke(query_input)
    logger.info(f"输出结果: {result}\n")