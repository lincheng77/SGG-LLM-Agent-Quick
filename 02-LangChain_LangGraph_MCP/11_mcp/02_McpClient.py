from loguru import logger
import json
from loguru import logger
import importlib


# 动态导入模块
module = importlib.import_module("01_McpServer")
# 获取 mcp 对象
mcp = module.mymcp


class MCPWeatherClient:
    def __init__(self, mcp_instance):
        self.mcp_instance = mcp_instance
        self.available_tools = mcp_instance._tools  # 获取服务端已注册的所有工具


    def check_tool_availability(self, tool_name: str) -> bool:
        is_available = tool_name in self.available_tools
        if is_available:
            logger.info(f"工具 '{tool_name}' 可用")
        else:
            logger.warning(f"工具 '{tool_name}' 未在服务端注册")
        return is_available

    def call_get_weather(self, city: str) -> str or None:
        tool_name = "get_weather"
        if not self.check_tool_availability(tool_name):
            return None
        try:
            weather_result = self.available_tools[tool_name](city)
            logger.info(f"成功获取 {city} 天气数据，返回结果长度：{len(weather_result)}")
            return weather_result
        except Exception as exc:
            logger.error(f"调用 {tool_name} 工具失败：{str(exc)}")
            return None


def run_client_demo():
    logger.info("初始化 MCP 天气客户端...")
    client = MCPWeatherClient(mcp)

    target_cities = ["Beijing", "Shanghai"]
    for city in target_cities:
        logger.info(f"\n========== 查询 {city} 天气 ==========")
        weather_data = client.call_get_weather(city)
        if weather_data:
            formatted_data = json.dumps(json.loads(weather_data), indent=4, ensure_ascii=False)
            print(f"格式化天气结果：\n{formatted_data}")
        print("-" * 50)



if __name__ == "__main__":
    logger.info("启动 MCP 天气客户端...")
    logger.warning("请确认 MCPWeatherServer 服务端已正常启动！")
    run_client_demo()