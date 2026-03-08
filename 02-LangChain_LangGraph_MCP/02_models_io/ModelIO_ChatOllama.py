from langchain_ollama import ChatOllama

import os
import dotenv

dotenv.load_dotenv()


API_URL = os.getenv("OLLAMA_API_URL")

model = ChatOllama(
    base_url=API_URL,
    model="modelscope.cn/unsloth/Qwen3.5-35B-A3B-GGUF:Q4_K_M",
    reasoning=False,
)

print(model.invoke("什么是LangChain，100字以内回答"))
