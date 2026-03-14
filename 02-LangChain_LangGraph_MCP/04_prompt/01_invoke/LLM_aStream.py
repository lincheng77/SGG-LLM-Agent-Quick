# 1.导入依赖
import os

import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_URL = os.getenv("QWEN_API_URL")

model = init_chat_model(
    model="qwen3.5-plus",
    model_provider="openai",
    api_key = API_KEY,
    base_url = API_URL
)


async def exe():
    response = model.astream("解释一下LangChain是什么，简洁回答100字以内")
    async for chunk in response:
        print(chunk.content, end="", flush=True)

async def main():
    task = asyncio.create_task(exe())

    print("异步调用开始：这里应该异步没执行完就打印出来了把？")

    await task

if __name__ == '__main__':
    asyncio.run(main())
