from typing import Annotated, TypedDict

Age = Annotated[int, "年龄，范围0-150"]


"""
TypedDict 只在类型检查工具里生效：
Python 运行时不会检查类型。
"""
class Person(TypedDict):
    name: str
    age: int
    age2:Age

p = Person(name="z3",age=111,age2=188)
print(p)

p = Person(name="z3",age="1111", age2="22222")
print(p)


