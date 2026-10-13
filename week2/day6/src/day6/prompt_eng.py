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

def llm_ans(prompt):
    message={
        "role":"user",
        "content":prompt
    }
    messages=[message]
    response=client.chat.completions.create(model=model,messages=messages)
    ans=response.choices[0].message.content
    return ans

bad_prompt="""
#Role:
You are a support assistent at a mobile/laptop company
#Task:
You have to classify the issue in a category
#Constraints:
You have to classify the issue in one of three categories namely billing,technical,return
#Output format:
Your answer should be in one word only . The one word should be one of the categories given in constraints
#Example:
For example if a user complain says he wants a refund then the category is return
Fallback:
If the issue is unrelated to any of the categories mentioned in constraints , then the answer should be other
This is user complaint:
My laptop is not working.
"""
print(llm_ans(bad_prompt))