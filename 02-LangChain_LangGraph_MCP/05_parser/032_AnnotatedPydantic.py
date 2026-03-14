from pydantic import BaseModel, Field
from typing import Annotated


Age = Annotated[int, Field(ge=0, le=150, description="年龄，范围0-150")]


"""
TypedDict 在类型检查工具里生效：
Python 运行时也会检查类型。
"""
class Person(BaseModel):
    name: str
    age: int
    age2:Age

p = Person(name="z3",age=111,age2=188)
print(p)

p = Person(name="z3",age="1111", age2="22222")
print(p)


