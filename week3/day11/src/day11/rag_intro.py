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

#knowledge base

knowlede_base={
    "age":25,
    "net worth":"net worth of pratyush is 2000"
}


#retreave releted info from knowlede_base and return to LLM.
def releated_info(question):
    question = question.lower()

    if "age" in question:
        return knowlede_base["age"]
    elif "net worth" in question:
        return knowlede_base["net worth"]
    else:
        return None

#LLM    
def ask_llm(question):
    context=releated_info(question)
    system_prompt=f""" answer should be in one line only. Answer only based on this context.do not hallucinate. Context:{context}"""
    system_message={
        "role":"system",
        "content":system_prompt
    }
    user_messages={
        "role":"user",
        "content":question
    }

    messages=[system_message,user_messages]

    response = client.chat.completions.create(model=model,messages=messages)
    answer = response.choices[0].message.content
    return answer

# ques="do you know who is padho with pratyush "
#ques="how old is pratyush narayan"

#ques="what is pratyush'age?"
#ques="what is pratyush'net worth?"

ques="how old are pratyush"
print(ask_llm(ques))

