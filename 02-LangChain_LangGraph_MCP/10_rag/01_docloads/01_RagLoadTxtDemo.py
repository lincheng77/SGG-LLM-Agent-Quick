from langchain_community.document_loaders import TextLoader

file_path = 'assets/sample.txt'
encoding = 'utf-8'

docs = TextLoader(file_path, encoding).load()

print(docs)