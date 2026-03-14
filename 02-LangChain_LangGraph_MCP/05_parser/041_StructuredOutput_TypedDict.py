
import os
from typing import TypedDict, Annotated
from langchain.chat_models import init_chat_model
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")

class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]

class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"] # List<Animal>


messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}]


model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)


llm_with_structured_output = model.with_structured_output(AnimalList)
print(f"llm_with_structured_output的内容是：{llm_with_structured_output}\n\n\n\n\n\n")
response = llm_with_structured_output.invoke(messages)
print(response)
print(type(response))

