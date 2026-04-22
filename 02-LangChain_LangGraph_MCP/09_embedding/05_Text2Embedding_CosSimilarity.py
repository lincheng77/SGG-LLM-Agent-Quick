import dashscope
import os
from http import HTTPStatus
import numpy as np
import os
import dotenv
import json

dotenv.load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")
API_RUL = os.getenv("QWEN_API_URL")

texts = [
    '我喜欢吃苹果',
    '苹果是我最喜欢吃的水果',
    '我喜欢用苹果手机'
]

embeddings = []

for text in texts:
    input_data = [{'text': text}]
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        api_key=API_KEY,
        base_url=API_RUL,
        input=input_data
    )

    if resp.status_code == HTTPStatus.OK:
        embedding = resp.output['embeddings'][0]['embedding']
        embeddings.append(embedding)

# 计算余弦相似度
def cosine_similarity(vec1, vec2):
    # 计算两个向量的余弦相似度
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


print("文本相似度比较结果:")
print("=" * 60)
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"文本{i+1} vs 文本{j+1}:")
        print(f"  文本{i+1}: {texts[i]}")
        print(f"  文本{j+1}: {texts[j]}")
        print(f"  余弦相似度: {similarity:.4f}")
        print("-" * 40)