from dotenv import load_dotenv
from langchain_core.exceptions import LangChainException
from langchain_openai import ChatOpenAI
import os

# 加载.env文件中的环境变量（指定编码，避免中文乱码）
load_dotenv(encoding='utf-8')

# 配置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
"""
__name__: 这是一个 Python 内置变量。
如果当前文件是直接运行的脚本，__name__ 的值是 "__main__"。
如果当前文件是被导入的模块（例如 my_module.py），__name__ 的值就是模块名（例如 "my_module"）
"""

def init_ll_client() -> ChatOpenAI:
    """
    初始化LLM客户端（封装乘函数，提高复用性）

    :return:
        ChatOpenAI： 初始化后的LLM客户端实例
    """

    # 1. 读取环境变量并做非空校验
    api_key = os.getenv("QWEN_API_KEY")
    if not api_key:
        raise  ValueError("环境变量 QWEN_API_KEY 未配置，请假差.env文件")

    # 2. 初始化LLM客户端（参数命名规范，添加注释）
    llm = ChatOpenAI(
        model="deepseek-v3.2",  # 模型名称
        api_key=api_key,  # 通义千问API密钥
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里云兼容接口地址
        temperature=0.7,  # 可选：添加温度参数，控制输出随机性
        max_tokens=2048  # 可选：限制输出长度，避免超限
    )

    return llm

def main():
    """主函数： 封装核心逻辑，符合Python工程化规范"""
    try:
        # 初始化客户端
        llm = init_ll_client()
        logger.info("LLM客户端初始化成功")

        # 调用模型
        question = "你是谁"
        response = llm.invoke(question)

        # 格式化输出结果
        logger.info(f"问题：{question}")
        logger.info(f"回答：{response.content}")

        print("\n====================以下是流式输出,另一种调用方式====================")


        responseStream = llm.stream("介绍下langchain。 300字以内")
        for chunk in responseStream:
            print(chunk.content, end="")

    # 捕获具体异常
    except ValueError as e:
        logger.error(f"配置错误：{str(e)}")
    except LangChainException as e:
        logger.error(f"模型调用失败：{str(e)}")
    except Exception as e:
        logger.error(f"未知错误：{str(e)}")

if __name__ == '__main__':
    main()