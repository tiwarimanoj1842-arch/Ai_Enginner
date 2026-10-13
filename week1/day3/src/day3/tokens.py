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
# prompt="Do you know Padho with Pratyush"

prompt1 = "Hi!"
prompt2 = "Explain Time Travel in Details"
prompt3 = "write a 1000 words essay on machine learning"

prompts = [prompt1,prompt2,prompt3]

for prompt in prompts:
    message={
    "role":role,
    "content":prompt
    }
    messages = [message]
    response=client.chat.completions.create(model=model,messages=messages , max_tokens=200)
    usage=response.usage
    print(f"Prompt : {prompt} ----> your token : {usage.prompt_tokens} -----> completion_tokens : {usage.completion_tokens} total token : {usage.prompt_tokens + usage.completion_tokens}  Finish reason : {response.choices[0].finish_reason}")


# message={
#     "role":role,
#     "content":prompt
# }

# messages = [message]
# response=client.chat.completions.create(model=model,messages=messages)

# answer = response.choices[0].message.content
# print(answer)
