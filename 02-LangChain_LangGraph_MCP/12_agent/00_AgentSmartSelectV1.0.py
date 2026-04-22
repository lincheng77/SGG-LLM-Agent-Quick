
import json
import httpx
from typing import TypedDict

import langchain
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
import os
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_API_URL = os.getenv("OPENWEATHER_API_URL")
print(langchain.__version__)

@tool
def get_weather(loc):
    """
    查询即时天气函数
    """
    # Step 1. 构建请求 URL
    url = OPENWEATHER_API_URL

    # Step 2. 设置查询参数，包括城市名、API Key、单位和语言
    params = {
        "q": loc,
        "appid": OPENWEATHER_API_KEY,  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3. 发送 GET 请求获取天气数据
    response = httpx.get(url, params=params,timeout=30)
    # Step 4. 解析响应内容为 JSON 并序列化为字符串返回
    data = response.json()
    return json.dumps(data)

# 结构化输出（推荐）
class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str


# 模型
model = init_chat_model(
    model="deepseek-v3.2",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)

# 创建Agent
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=(
        "你是天气助手。"
        "当用户询问多个城市天气时，"
        "你需要分别调用工具获取数据，并进行比较分析。"
    ),
    response_format=WeatherCompareOutput, #需要模型支持，阿里的模型不太行
)

# 调用Agent
result = agent.invoke(
    {"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"}
)

print(result)
print(json.dumps(result["structured_response"], ensure_ascii=False, indent=2))