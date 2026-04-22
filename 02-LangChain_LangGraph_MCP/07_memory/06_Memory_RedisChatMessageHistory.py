from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from loguru import logger
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableWithMessageHistory, RunnableConfig
import os
import redis
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")
REDIS_URL = os.getenv("REDIS_URL")


redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# 模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)

# 提示词
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("history"),
    ("human", "{question}")
])


# 历史
def get_session_history(session_id: str) -> RedisChatMessageHistory:
    """获取或创建会话历史（使用 Redis）"""
    # 创建 Redis 历史对象
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
    )
    return history


# 执行链
chain = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)
config = RunnableConfig(configurable={"session_id": "user-001"})


# 对话
print("开始对话（输入 'quit' 退出）")
while True:
    question = input("\n输入问题：")
    if question.lower() in ['quit', 'exit', 'q']:
        break

    response = chain.invoke({"question": question}, config)
    logger.info(f"AI回答:{response.content}")

    # 等同于redis-cli的SAVE命令，强制写入dump.rdb
    redis_client.save()