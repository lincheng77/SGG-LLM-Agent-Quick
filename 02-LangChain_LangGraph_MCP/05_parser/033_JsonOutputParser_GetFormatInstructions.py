from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from langchain.chat_models import init_chat_model
from loguru import logger
from pydantic import BaseModel, Field
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")


"""
BaseModel 来自 Pydantic 库。
它的作用是：
    用 Python 类定义数据结构，并自动进行数据校验和解析

当你继承它时，Pydantic 会帮你自动实现：
    数据类型检查
    数据解析
    JSON 转换
    错误提示
"""

# 解析器配置
class Person(BaseModel):
    """
    定义一个新闻结构化的数据模型类
    属性:
        time (str): 新闻发生的时间
        person (str): 新闻涉及的人物
        event (str): 发生的具体事件
    """
    time: str = Field(description="时间") #
    person: str = Field(description="人物")
    event: str = Field(description="事件")

parser = JsonOutputParser(pydantic_object=Person)
format_instructions = parser.get_format_instructions()
print(f"format_instructions的内容是：{format_instructions}\n\n\n\n\n\n")
"""
    format_instructions相当于是一个帮你补充提示词的要求和范例，根据你的pydantic_object
"""

# 提示词
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，你只能输出结构化JSON数据。"),
    ("human", "请生成一个关于{topic}的新闻。{format_instructions}")
])
prompt = template.format_messages(topic="小米su7跑车", format_instructions=format_instructions)


# 模型
model = init_chat_model(
    model="qwen3.5-27b",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_RUL
)

# 输出
result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result}")
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")

"""
LangChain Output Parser 区别

Parser                 输出结果
------------------------------------------------
JsonOutputParser       dict（JSON → Python字典）
PydanticOutputParser   Pydantic模型实例（BaseModel对象）
"""