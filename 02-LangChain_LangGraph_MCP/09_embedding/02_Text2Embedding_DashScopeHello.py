import dashscope
from http import HTTPStatus
import os
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")

input_text = "衣服的质量杠杠的"

# 只支持 文本 → 向量
resp = dashscope.TextEmbedding.call(
    model="text-embedding-v4",
    api_key=API_KEY,
    input=input_text,
)

if resp.status_code == HTTPStatus.OK:
    print(resp)