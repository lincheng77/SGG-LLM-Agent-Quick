from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

chatPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="你是AI助手，你的名字叫{name}。"),
        HumanMessage(content="请问：{question}")
    ]
)



message = chatPrompt.format_messages(name="和郝凤", question="什么是LangChain")

print(message)


###################################################这个代码其实填充不进去！！！！！！！！！！！！！！#######################################
# 原因说明：
#
# 1. ChatPromptTemplate.from_messages() 在设计时主要是用于接收“模板消息”，
#    也就是带有变量占位符的提示模板。
#
# 2. 但是这里我们传入的是已经实例化好的消息对象：
#       SystemMessage(...)
#       HumanMessage(...)
#
# 3. 当 LangChain 解析 from_messages() 参数时，如果传入的是 Message 对象，
#    它会把它们当成“已经构建完成的消息”，而不是“模板”。
#
# 4. 这样 LangChain 在内部构建 PromptTemplate 时，
#    就不会正确提取模板变量 {name} 和 {question}。
#
# 5. 由于变量没有被识别为模板变量，
#    format_messages() 在执行时就无法正确替换这些变量，
#    导致看起来像是“模板变量填充不进去”。
#
# 6. 简单来说：
#       SystemMessage / HumanMessage 在这里被当成普通消息对象，
#       而不是可格式化的 Prompt 模板。
#
# 7. 因此虽然字符串中写了 {name} 和 {question}，
#    但 LangChain 并没有把它们当作模板变量处理，
#    format_messages() 也就无法正常完成变量填充。
############################################################################################################