import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"
role="user"

from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""
Extract the personal information from the Ticket strictly based on this schema and give a json output.
{schema}
"""

message_system={
    "role": "system",
    "content":system_prompt
}

text="Hello my name is Prythush.I have a iphone which is not working at all.My address is delhi.My email is abc@gmail.com.My contach number is 38884332"
prompt=f"""
This is a customer ticket . please extract this personal information from this.
{text}
"""

message={
    "role":role,
    "content":prompt
}

messages = [message_system,message]
response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)

answer = response.choices[0].message.content
print(answer)

# isko padhete kaise hai
import json
rwa_json=answer
data_file=json.loads(rwa_json)
ticket=Ticket(**data_file)

# isko pass kar sakte hai aage
print(ticket.name)
print(ticket.email)
print(ticket.issue)


