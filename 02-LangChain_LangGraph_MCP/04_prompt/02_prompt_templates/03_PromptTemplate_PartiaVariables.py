import os

from datetime import datetime
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import dotenv

dotenv.load_dotenv(encoding="utf-8")

"""
partial 就是预设默认值，可以被覆盖！
"""

# 模板1
template = PromptTemplate.from_template(
    template="现在时间是：{time},请对我的问题给出答案，我的问题是：{question}",
    partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
)
prompt = template.format(question="今天是几号？")
print(prompt)

# 模板2
template = PromptTemplate.from_template(
    template="现在时间是：{time},请对我的问题给出答案，我的问题是：{question}",

)
template = template.partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 注意需要一个接收值！
prompt = template.format(question="今天是几号呢？")
print(prompt)

# 模板3
template = PromptTemplate(
    template="{foo} {bar}",
    input_variables=["foo", "bar"],
    partial_variables={"foo": "hello"},  # 预先定义部分变量foo值为hello
)
prompt = template.format(bar="world")
print(prompt)
prompt = template.format(foo="李四", bar="world")
print(prompt)
