from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
import dotenv
import json

from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")
REDIS_URL = os.getenv("REDIS_URL")




# 模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)

# 提示词
prompt_template = """
    请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，
    如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。

    文本内容：
    {context}

    问题：{question}

    回答：
    "
"""
prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)


# Embedding 模型
embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=API_KEY
)



# 加载分割文档
# loader = Docx2txtLoader("alibaba-java.docx")  # LangChain提供了Docx2txtLoader专门用于加载.docx文件，先通过pip install docx2txt
loader = UnstructuredLoader("alibaba-java.docx")  # 直接传入文件路径即可
documents = loader.load()
# RecursiveCharacterTextSplitter LangChain 推荐使用的切分器。它会 优先按语义边界切：
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
texts = text_splitter.split_documents(documents)
print(f"文档个数:{len(texts)}")


# 配置Redis连接参数和索引名称
config = RedisConfig(
    index_name="my_index4",
    redis_url=REDIS_URL,
)
vector_store = RedisVectorStore(embeddingsModel, config=config)
# 将文本和元数据添加到向量存储中
vector_store.add_documents(texts)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})


chain = {
    "context": retriever,
    "question": RunnablePassthrough()
} | prompt | model


question = "00000和A0001分别是什么意思"
result = chain.invoke(question)
print("\n问题:", question)
print("\n回答:", result.content)