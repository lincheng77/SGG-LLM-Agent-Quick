from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser, JsonOutputKeyToolsParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from loguru import logger
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnableWithMessageHistory, RunnableConfig
import redis
import importlib
weather_module = importlib.import_module("04_QueryWeatherTool")
get_weather = weather_module.get_weather

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
model = model.bind_tools([get_weather])


# 模型 -> 解析器 -> 调用天气工具
parser = JsonOutputKeyToolsParser(
    key_name=get_weather.name,
    first_tool_only=True #只解析第一个 tool 调用
)
weather_chain = model | parser | get_weather


# 提示模板 -> 模型 -> 输出解析器
prompt = PromptTemplate.from_template(
    """你将收到一段 JSON 格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。
    以下是天气 JSON 数据：
    请将其转换为中文天气描述，例如：
    “北京现在天气：多云，气温 28℃，体感有点闷热（约 32℃），湿度 75%，微风（东南风 2 米/秒），
    能见度很好，大约 10 公里。建议穿短袖短裤。适合做户外运动。"
    """
)
output_parser = StrOutputParser()
chain = prompt | model | output_parser


full_chain = weather_chain | (lambda x: {"weather_json": x}) | chain
result = full_chain.invoke("请问北京今天的天气如何？")
logger.info(result)
