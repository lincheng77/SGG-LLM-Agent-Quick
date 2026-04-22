import json
import os
import httpx
from loguru import logger
import os
import dotenv
dotenv.load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_API_URL = os.getenv("OPENWEATHER_API_URL")

class MCPWeatherServer:
    def __init__(self, name: str, host: str, port: int):
        self.name = name
        self.host = host
        self.port = port
        self._tools = {} # 存储注册的工具函数，支撑 @mcp.tool() 装饰器


    def tool(self):
        def decorator(func):
            self._tools[func.__name__] = func  # 注册工具函数
            return func

        return decorator


    def run(self, transport: str):
        if transport != "sse":
            logger.warning(f"不支持的传输协议 {transport}，默认使用 SSE")
        logger.info(f"启动 MCP SSE 天气服务器，监听 http://{self.host}:{self.port}/sse")
        self._keep_alive()


    def _keep_alive(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("MCP 天气服务器已停止")

mymcp = MCPWeatherServer("WeatherServerSSE", host="127.0.0.1", port=8000)


@mymcp.tool()
def get_weather(city: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }
    resp = httpx.get(url, params=params, timeout=10)
    data = resp.json()
    logger.info(f"查询 {city} 天气结果：{data}")
    return json.dumps(data, ensure_ascii=False)

if __name__ == "__main__":
    logger.info("启动 MCP SSE 天气服务器，监听 http://127.0.0.1:8000/sse")
    mymcp.run(transport="sse")