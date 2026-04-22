from langchain_core.tools import tool
import json
import os
import httpx
import dotenv
dotenv.load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_API_URL = os.getenv("OPENWEATHER_API_URL")


@tool
def get_weather(loc):
    """
    查询即时天气函数
    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
                则 loc 参数需要输入 'Beijing'/'shanghai'。
    :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
             https://home.openweathermap.org/users/sign_in。
             返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式进行表示，
             其中包含了全部重要的天气信息。
    """

    params = {
        "q": loc,
        "appid": OPENWEATHER_API_KEY,  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    response = httpx.get(OPENWEATHER_API_URL, params=params, timeout=30)

    data = response.json()
    print(data)
    print(json.dumps(data))
    return json.dumps(data)

result = get_weather.invoke("beijing")
print(result)