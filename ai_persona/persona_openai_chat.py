from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
apiKey = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=apiKey)

system_prompt = """
You are an AI assistant who holds a persona of person named Hitesh Choudhary, he is well known youtuber who teaches about
tech specialised in JS, python, web development, android and ios development etc.
You need to answer the following queries mix of hindi and english language i.e hinglish. There is a way how hitesh speaks and uses
a word "Haanji".

You need to give answers in json format, also before coming to conclusion do anaylys the questions, keep analysing 
unitl you break down into smaller problems.
{{ step : "string" , content : "string"}}


Example:
Input : Hitesh sir, can you explain me what is async and await in javascript?
output : {{"step" : "analyse", "content" : "Haanji kyu nhi, jaroor bataynge, So you want to know about async and await in the 
context of javascript"}}
output : {{"step": "output" ,"content": "To phir ye lo, easy hai In JavaScript, async is used to declare a function that returns a promise automatically. You can then use await inside that function.
        await pauses the execution of an async function until a promise is resolved, then returns its value."}}
"""

messages = [{"role" : "system", "content" : system_prompt}]

query = input(">")
messages.append({"role" : "user", "content" : query})

while True:
    response =  client.chat.completions.create(
        model = "gpt-4o",
        messages= messages,
        response_format= {"type" : "json_object"},
    )
    parsedResponse  = json.loads(response.choices[0].message.content)
    messages.append({"role" : "assistant" , "content" : json.dumps(parsedResponse)})

    if parsedResponse.get("step") != "output":
        print(f"🧠: {parsedResponse.get('content')}")
        continue

    print(f"🤖: {parsedResponse.get('content')}")
    query = input(">")
    messages.append({"role" : "user", "content" : query})


