import dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
import os

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


# 提示词
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我提出的问题"),
    ("human", "请回答:{question}")
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


chain = chat_prompt | model | parser
result= chain.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
logger.info(f"Chain执行结果:\n {result}")
logger.info(f"Chain执行结果类型: {type(result)}")