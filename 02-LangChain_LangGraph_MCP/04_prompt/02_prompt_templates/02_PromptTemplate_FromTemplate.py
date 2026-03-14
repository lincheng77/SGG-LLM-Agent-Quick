import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import dotenv
dotenv.load_dotenv(encoding="utf-8")

# 模型
API_KEY = os.getenv("QWEN_API_KEY")
API_URL = os.getenv("QWEN_API_URL")
model = init_chat_model(
    model="qwen3.5-plus",
    model_provider="openai",
    api_key=API_KEY,
    base_url=API_URL,
)

# 提示词
template = PromptTemplate.from_template("你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}")

# 1.
prompt = template.format(role="python开发",question="快速排序怎么写？")
print(prompt)

# 2.
prompt = template.format_prompt(role="python开发",question="快速排序怎么写？")
print(prompt)
print(prompt.to_messages())
print("\n\n")


# 3.
result = (template | model).invoke({"role": "python开发", "question": "快速排序怎么写？"}) #输入必须是字典！
print(result.content)
print("\n\n")

"""
# -----------------------------------------------------------------------------
# 方法对比说明：
# -----------------------------------------------------------------------------
# 1. .format() 
#    - 返回值: str (字符串)
#    - 作用: 直接将变量填入模板，返回最终的纯文本提示词。
#    - 场景: 当你只需要最终的提示词文本，例如打印调试、日志记录、
#            或手动构建消息时使用。
#
# 2. .format_prompt() 
#    - 返回值: PromptValue (对象)
#    - 作用: 返回一个结构化的 Prompt 对象，而不是普通字符串。
#            该对象可以根据需要转换为不同格式：
#            - .to_messages() -> [HumanMessage, SystemMessage, ...]
#            - .to_string()   -> str
#
# 3. .invoke()
#    - 返回值: PromptValue（对于 PromptTemplate / ChatPromptTemplate）
#    - 作用: 按照 Runnable 接口执行模板，将输入变量填充到 Prompt 中，
#            并返回可直接传递给下游组件（如 LLM）的 PromptValue。
#    - 场景: 在 LangChain LCEL 或 Runnable 管道中统一调用组件时使用，例如：
#
#            chain = prompt | model | parser
#            chain.invoke({"name": "Tom"})
#
# -----------------------------------------------------------------------------
# 总结：
# -----------------------------------------------------------------------------
# .format()        -> 返回字符串 (str)
# .format_prompt() -> 返回 PromptValue
# .invoke()        -> Runnable 执行方式，返回 PromptValue（适合链式调用）
# -----------------------------------------------------------------------------
"""



