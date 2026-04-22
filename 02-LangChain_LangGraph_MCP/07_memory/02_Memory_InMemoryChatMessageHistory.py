from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
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

# 历史
history = InMemoryChatMessageHistory()
history.add_user_message("我叫张三，我的爱好是学习")

# 调用
ai_message = model.invoke(history.messages)
logger.info(f"第一次回答\n{ai_message.content}")


history.add_user_message("我叫什么？我的爱好是什么？")
ai_message2 = model.invoke(history.messages)
logger.info(f"第二次回答\n{ai_message2.content}")


# 最终
history.add_message(ai_message2)
for message in history.messages:
    logger.info(message.content)