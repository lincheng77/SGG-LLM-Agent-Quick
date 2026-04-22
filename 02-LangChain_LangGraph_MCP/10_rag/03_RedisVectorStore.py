
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
import dotenv
import json

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")
REDIS_URL = os.getenv("REDIS_URL")

# 1. 初始化阿里千问 Embedding 模型
embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=API_KEY
)

texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]

'''下面的注释代码 仅供打印使用'''
# embeddings = embeddingsModel.embed_documents(texts)
#
#
# # 1 是 enumerate() 函数的第二个参数，用于指定计数的起始值
# for i, vec in enumerate(embeddings, 1):
#     print(f"文本 {i}: {texts[i-1]}")
#     print(f"向量长度: {len(vec)}")
#     print(f"前5个向量值: {vec[:5]}\n")


# 定义每条文本对应的元数据信息
metadata = [{"segment_id": "1"}, {"segment_id": "2"}, {"segment_id": "3"}]

# 配置Redis连接参数和索引名称
config = RedisConfig(
    index_name="newsgroups",
    redis_url=REDIS_URL,
)
vector_store = RedisVectorStore(embeddingsModel, config=config)

# 将文本和元数据添加到向量存储中
ids = vector_store.add_texts(texts, metadata)
print(ids[0:5])