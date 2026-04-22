from typing import Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy


class AtguiguState(TypedDict):
    result: str


# 全局计数器：记录API尝试次数
attempt_counter = 0

# 定义图、节点、边
def build_retry_graph(node_name: str, node_func, retry_policy: RetryPolicy):
    builder = StateGraph(AtguiguState)

    builder.add_node(node_name, node_func, retry_policy=retry_policy)

    builder.add_edge(START, node_name)
    builder.add_edge(node_name, END)

    return builder.compile()


# 模拟不稳定的API调用，使用全局变量跟踪尝试次数
def unstable_api_call(state: AtguiguState) -> Dict[str, Any]:
    """模拟不稳定API：前2次失败，第3次成功（全局计数器记录尝试次数）"""
    global attempt_counter
    attempt_counter += 1
    print(f"尝试调用API，这是第 {attempt_counter} 次尝试")

    if attempt_counter < 3:
        raise Exception(f"模拟API调用失败abcd (尝试 {attempt_counter})")
    return {"result": f"API调用成功，经过 {attempt_counter} 次尝试"}

# 自定义重试条件判断函数
def custom_retry_on(exception: Exception) -> bool:
    print("########################:  "+str(exception))
    err_msg = str(exception)
    if "模拟API调用失败" in err_msg:
        print(f"捕获到可重试异常: {err_msg}")
        return True
    print(f"捕获到不可重试异常: {err_msg}")
    return False

# 模拟抛出 ValueError 的节点
def value_error_call(state: AtguiguState) -> Dict[str, Any]:
    print("调用会抛出 ValueError 的节点")
    raise ValueError("模拟 ValueError 异常")


# 测试方法1：默认重试策略
def test_default_retry():
    global attempt_counter
    print("1. 使用默认重试策略:")
    print("   默认策略会对除特定异常外的所有异常进行重试")
    print("   不会重试的异常包括: ValueError, TypeError, ArithmeticError, ImportError,")
    print("                     LookupError, NameError, SyntaxError, RuntimeError,")
    print("                     ReferenceError, StopIteration, StopAsyncIteration, OSError\n")

    print("测试默认重试策略:")
    attempt_counter = 0  # 重置计数器
    default_graph = build_retry_graph(
        node_name="unstable_api",
        node_func=unstable_api_call,
        retry_policy=RetryPolicy(max_attempts=5)  # 最多5次尝试，足够重试成功
    )
    try:
        result = default_graph.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:
        print(f"最终失败: {type(e).__name__}: {e}\n")


# 测试方法2：自定义重试策略（输出完全匹配要求）
def test_custom_retry():
    global attempt_counter
    print("2. 使用自定义重试策略:")
    print("   自定义策略只对特定错误进行重试\n")
    print("测试自定义重试策略:")
    attempt_counter = 0  # 重置计数器
    custom_graph = build_retry_graph(
        node_name="custom_retry_api",
        node_func=unstable_api_call,
        retry_policy=RetryPolicy(max_attempts=5, retry_on=custom_retry_on)
    )
    try:
        result = custom_graph.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:
        print(f"最终失败: {type(e).__name__}: {e}\n")


# 测试方法3：不可重试异常演示,测试 ValueError（默认策略不会重试）
def test_no_retry_exception():
    print("3. 测试不会重试的异常类型:")
    print("测试 ValueError（默认策略不会重试）:")
    no_retry_graph = build_retry_graph(
        node_name="value_error_node",
        node_func=value_error_call,
        retry_policy=RetryPolicy(max_attempts=3)
    )
    try:
        result = no_retry_graph.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:
        print(f"最终失败: {type(e).__name__}: {e}\n")



if __name__ == "__main__":
    print("=== LangGraph 节点重试策略完整演示===")
    print("-" * 80 + "\n")
    # test_default_retry()
    # test_custom_retry()
    test_no_retry_exception()
    print("-" * 80)
    print("=== 演示结束 ===")