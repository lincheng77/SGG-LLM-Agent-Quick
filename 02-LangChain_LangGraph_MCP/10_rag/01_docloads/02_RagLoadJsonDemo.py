from langchain_community.document_loaders import TextLoader, JSONLoader



docs = JSONLoader(
    file_path = 'assets/sample.json',
    jq_schema=".", # 提取所有字段
    text_content=False # 提取内容是否为字符串格式

).load()

print(docs)
