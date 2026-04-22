from typing import Annotated, List, Sequence
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


# 定义状态
class AtguiguState(TypedDict):
    subjects: List[str]
    jokes: Annotated[List[str], lambda x, y: x + y]  # 使用列表合并的方式


def generate_subjects(state: AtguiguState) -> dict:
    print("执行节点(第一个节点：生成需要处理的主题列表): generate_subjects")
    subjects = ["猫", "狗", "程序员"]
    print(f"生成主题列表: {subjects}")
    return {"subjects": subjects}


# Map节点
def make_joke(state: AtguiguState) -> dict:

    subject = state.get("subject", "未知")
    print(f"执行节点: make_joke，处理主题: {subject}")

    # 根据主题生成相应笑话
    jokes_map = {
        "猫": "为什么猫不喜欢在线购物？因为它们更喜欢实体店！",
        "狗": "为什么狗不喜欢计算机？因为它们害怕被鼠标咬！",
        "程序员": "为什么程序员喜欢洗衣服？因为他们在寻找bugs！",
        "未知": "这是一个关于未知主题的神秘笑话。"
    }

    joke = jokes_map.get(subject, f"这是一个关于{subject}的即兴笑话。")
    print(f"生成笑话: {joke}")
    return {"jokes": [joke]}

def map_subjects_to_jokes(state: AtguiguState) -> List[Send]:

    print("执行条件边函数: map_subjects_to_jokes")
    subjects = state["subjects"]
    print(f"映射主题到joke任务: {subjects}")


    send_list = [Send("make_joke", {"subject": subject}) for subject in subjects]
    print(f"生成Send对象列表: {send_list}")
    return send_list




# 创建图
builder = StateGraph(AtguiguState)

# 添加节点
builder.add_node("generate_subjects", generate_subjects)
builder.add_node("make_joke", make_joke)

# 开始边
builder.add_edge(START, "generate_subjects")

# 添加send边（多路并发边）
builder.add_conditional_edges(
    "generate_subjects",
    map_subjects_to_jokes
)

# 结束边
builder.add_edge("make_joke", END)

# 编译图
graph = builder.compile()
print(graph.get_graph().print_ascii())

# 执行图
initial_state = {"subjects": [], "jokes": []}
print("初始状态:", initial_state)
result = graph.invoke(initial_state)
print(f"\n最终结果: {result}")



print(graph.get_graph().print_ascii())