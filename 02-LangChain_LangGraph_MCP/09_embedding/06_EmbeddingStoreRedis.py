import os
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document
import dotenv
import json

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")
REDIS_URL = os.getenv("REDIS_URL")


embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=API_KEY  # 从环境变量读取
)

# 2. 准备要向量化的文本（Document 列表）
texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis 是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。"
]
documents = [Document(page_content=text, metadata={"source": "manual"}) for text in texts]


# 3. 连接到 Redis 并存入向量（自动调用 embeddings 嵌入）
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url=REDIS_URL,                    # 替换为你的 Redis 地址
    index_name="my_index11",                # 向量索引名称
)


retriever = vector_store.as_retriever(search_kwargs={"k": 2})
results = retriever.invoke("LangChain 和 Redis 怎么结合？")
for res in results:
    print(res.page_content)


"""
metadata 是 文档的附加信息（标签 / 属性）。{"source": "manual"}这段文本来自 manual（手册）
search_kwargs 是 检索参数配置。     search_kwargs={"k": 2}每次检索返回最相似的 2 条文档
"""