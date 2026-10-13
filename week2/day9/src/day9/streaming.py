import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-20b"

user_prompt="Explain the all about internet"

user_messages={
    "role":"user",
    "content":user_prompt
}


messages = [user_messages]

response = client.chat.completions.create(model=model , messages=messages,stream=True)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="" , flush=True)

print()