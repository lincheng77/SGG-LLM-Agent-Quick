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
    ("system", "你是一个友好的中文助理，会根据上下文回答问题。"),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

parser = StrOutputParser()

chain = prompt | model | parser


history = InMemoryChatMessageHistory()
# 定义全局的“会话存储”，用来保存每个 session 的聊天历史
#    （真实项目中可改为 Redis、SQLite 等）
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
runnable = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="question",  # 指定输入键
    history_messages_key="history"  # 指定历史消息键
)
history.clear()

# 模拟一个会话，用 session_id 区分不同用户
cfg = {"configurable": {"session_id": "user-001"}}
# 第一次提问：告诉模型“我叫张三”
print("用户：我叫张三。")
print("AI：", runnable.invoke({"question": "我叫张三。"}, cfg))
# 第二次提问：让模型回忆前面的对话
print("\n 用户：我叫什么？")
print("AI：", runnable.invoke({"question": "我叫什么？"}, cfg))