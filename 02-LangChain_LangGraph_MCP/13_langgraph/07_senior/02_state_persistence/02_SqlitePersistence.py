"""

pip install langgraph-checkpoint-sqlite
"""

import sqlite3
import operator
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph,START,END


class MyState(TypedDict):
    messages:Annotated[list,operator.add]

def node_1(state:MyState):
    return {"messages":["abc","def"]}


conn = sqlite3.connect(database="./sqlite_data.db",check_same_thread=False)
sqliteDB = SqliteSaver(conn=conn)

builder = StateGraph(MyState)

builder.add_node("node_1",node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile(checkpointer=sqliteDB)


config = {"configurable": {"thread_id": "user-001"}}
initial_state = graph.get_state(config)
print(f"Initial state: {initial_state}")
result = graph.invoke({"messages":[]}, config)
print(f"Result: {result}")


print()
print("====================查看执行后的状态====================")
# 查看执行后的状态
final_state = graph.get_state(config)
print()
print(f"Final state: {final_state}")

conn.close()