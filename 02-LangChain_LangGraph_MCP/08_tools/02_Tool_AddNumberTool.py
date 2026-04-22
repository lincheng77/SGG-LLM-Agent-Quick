
from langchain.tools import tool

'''
使用@tool装饰器
装饰器默认使用函数名称作为工具名称，但可以通过参数name_or_callable 来覆盖此设置。
同时，装饰器将使用函数的文档字符串作为工具的描述，因此函数必须提供文档字符串
'''
@tool
def add_number(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

result = add_number.invoke({"a": 1, "b": 12})

print(result)

print()

print(f"{add_number.name=}\n{add_number.description=}\n{add_number.args=}")



