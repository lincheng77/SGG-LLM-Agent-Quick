from langchain_ollama import ChatOllama

import os
import dotenv

dotenv.load_dotenv()


API_URL = os.getenv("OLLAMA_API_URL")

model = ChatOllama(
    base_url=API_URL,
    model="qwen3.5:9b",
    reasoning=False,
)

print(model.invoke("什么是LangChain，100字以内回答"))
