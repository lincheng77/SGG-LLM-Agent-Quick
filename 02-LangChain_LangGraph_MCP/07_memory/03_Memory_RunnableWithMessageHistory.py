from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from loguru import logger
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableWithMessageHistory, RunnableConfig
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


prompt = ChatPromptTemplate.from_messages([
    # 用于插入历史消息
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

parser = StrOutputParser()

chain = prompt | model | parser


history = InMemoryChatMessageHistory()
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,
    input_messages_key="input",  # 指定输入键
    history_messages_key="history"  # 指定历史消息键
)
history.clear()

config = RunnableConfig(configurable={"session_id": "user-001"})
logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))