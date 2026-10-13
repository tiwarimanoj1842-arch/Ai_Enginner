import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

def get_product_price(product):
    if(product=='iPhone 17'):
        return 1000
    elif product=='iPhone 15':
        return 500
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"

tools = {
    "get_product_price":get_product_price,
    "calculator":calculator
}

system_prompt="""
You are a shopping assistent.

You have these tools:

get_product_price(product)
calculator(expression)
IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000-1000")

Never write:
calculator(expression="5000-1000")

Follow these rules:

1.Decide what you need to do next.
2.Call ONLY ONE tool at a time.
3.After writing an action , STOP immediately.
4.Never guess or invent a tool result.
5.Wait until you recieve an Observation.
6.Then decide your next action.
7.When the task is complete,give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer:your answer
"""



def run_agent(question):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):
        print("\n---------------------")
        print(f"STEP {step + 1}")
        print("---------------------")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content or ""
        print(answer)

        # Agent has finished
        if "Final Answer:" in answer:
            break

        # Find the Action
        match = re.search(
            r'Action:\s*(\w+)\((.*?)\)',
            answer,
            re.DOTALL
        )

        if not match:
            print("Action nahi mila. Agent ko stop kar rahe hain.")
            break

        tool_name = match.group(1)
        tool_input = match.group(2).strip().strip('"').strip("'")

        # Run the tool
        if tool_name in tools:
            try:
                observation = tools[tool_name](tool_input)
            except Exception as e:
                observation = f"Tool error: {e}"
        else:
            observation = "Tool not found"

        print("Observation:", observation)

        # Add assistant response to conversation
        messages.append({
            "role": "assistant",
            "content": answer
        })

        # Give tool result back to the model
        messages.append({
            "role": "user",
            "content": f"Observation: {observation}\nContinue solving the original question."
        })

        sleep(2)




prompt="""
I have 5000 rupees.What is the price of an iphone 17?
and how much money will I have left?
"""

run_agent(prompt)
    