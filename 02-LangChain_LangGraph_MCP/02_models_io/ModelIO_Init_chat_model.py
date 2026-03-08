# 1.导入依赖
import os
from langchain.chat_models import init_chat_model
import dotenv
dotenv.load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_URL")
# 2.实例化模型
model = init_chat_model(
    model="deepseek-chat",
    api_key=API_KEY,
    base_url=API_URL
)

# 3.调用模型
print(model.invoke("你是谁").content)