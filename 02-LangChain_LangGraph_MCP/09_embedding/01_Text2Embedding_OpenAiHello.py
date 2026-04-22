
from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


input_text = "衣服的质量杠杠的"

client = OpenAI(
    api_key=API_KEY,
    base_url=API_RUL
)


completion = client.embeddings.create(
    model="text-embedding-v4",
    input=input_text
)


print(completion.model_dump_json())