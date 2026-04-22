import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

class State(TypedDict):
    x: int
    result: int


# 创建图
builder = StateGraph(State)


def expensive_node(state: State) -> dict[str, int]:
    time.sleep(3)
    return {"result": state["x"] * 2}

# 节点
builder.add_node(node="expensive_node",
                 action=expensive_node,
                 cache_policy=CachePolicy(ttl=8) #这个节点的结果缓存 8 秒
                 )

# 入口、出口
builder.set_entry_point("expensive_node")
builder.set_finish_point("expensive_node")
# 上面和下面其实是等价的，上面是隐式边，下面是显式边
# builder.add_edge(START, "expensive_node")
# builder.add_edge("expensive_node", END)

app = builder.compile(cache=InMemoryCache())



# 打印图的可视化结构
print(app.get_graph().print_ascii())


print("第一次执行（无缓存，耗时3秒）：")
print(app.invoke({"x": 5}))

print("第二次运行利用缓存并快速返回：")
print(app.invoke({"x": 5}))

time.sleep(8)
print("8秒后第三次执行（重新计算，耗时3秒）：")
print(app.invoke({"x": 5}))