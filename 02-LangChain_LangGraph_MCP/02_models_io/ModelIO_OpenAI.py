# Please install OpenAI SDK first: `pip install openai`
import os

from openai import OpenAI
import dotenv
dotenv.load_dotenv()


API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv("DEEPSEEK_API_URL")

client = OpenAI(
    api_key= API_KEY,
    base_url= API_URL,
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello,你是谁"},
    ],
    stream=False,

)

print(response.choices[0].message.content)