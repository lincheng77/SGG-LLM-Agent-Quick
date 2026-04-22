import dashscope
from http import HTTPStatus
import os
import dotenv
import json

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")

input_text = "衣服的质量杠杠的"

# 支持 多种数据类型 → 向量
resp = dashscope.MultiModalEmbedding.call(
    model="tongyi-embedding-vision-plus",  # 支持 v1 或 v2
    api_key=API_KEY,
    input=[{"text": "尚硅谷AI"}]
)

result = ""
# 处理模型返回结果，提取关键信息并格式化输出
if resp.status_code == HTTPStatus.OK:
    result = {
        "status_code": resp.status_code,
        "request_id": getattr(resp, "request_id", ""),
        "code": getattr(resp, "code", ""),
        "message": getattr(resp, "message", ""),
        "output": resp.output,
        "usage": resp.usage
    }
    print(json.dumps(result, ensure_ascii=False, indent=4))
