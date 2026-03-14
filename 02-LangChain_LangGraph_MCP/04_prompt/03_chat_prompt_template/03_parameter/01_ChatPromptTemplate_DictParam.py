from langchain_core.prompts import ChatPromptTemplate

chatPrompt = ChatPromptTemplate.from_messages(
    [
        {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
        {"role": "user", "content": "请问：{question}"}
    ]
)

message = chatPrompt.format_messages(name="小问", question="什么是LangChain")

print(message)