from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
apiKey = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=apiKey)

system_prompt = """You are an AI assistant who is specialized in answering all types of queries. 

But there are steps that you need to follow before you give the ouput, the steps are :
1. You need to analyse the question.
2. You need to think about the question, 
if question is complex then think as many time untill you break it into smaller problems, do repeat this step do each operation
individually explaining each step.
3. You need to give the output.
4. You need to validate the output.

Output should be in this json format :
{{ step : "string" , content : "string"}}

Example :
Input : What is 2+2*5?
output : {{step : "analyse", content : "Great, this is a mathematical question, user is interested to know about only mathematical question"}}
output : {{step : "think", content : "To perform the operation, I should follow bodmas rule, here first I will do multiplication operation and then addition"}}
output : {{step : "output" , content : "4"}}
output : {{step : "validate, content : "seems like 12 is correcr answer"}}

"""
messages = [{"role": "system", "content": system_prompt}]

query = input(">")
messages.append({"role": "user", "content" : query})
while True:
    response =  client.chat.completions.create(
        model= "gpt-4o",
        response_format= {"type" : "json_object"},
        messages= messages
    )
    parser_json_respone = json.loads(response.choices[0].message.content)
    messages.append({"role" : "assistant" , "content" : json.dumps(parser_json_respone)})
    
    if(parser_json_respone.get("step") != "output"):
        print(f"Brain : {parser_json_respone.get('content')}")
        continue
    print(f"Bot : {parser_json_respone.get('content')}")
    break

