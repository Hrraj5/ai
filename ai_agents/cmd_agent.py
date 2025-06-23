from openai import OpenAI
from dotenv import load_dotenv
import os
import json



load_dotenv()
apiKey = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=apiKey)

def cmdAgent(command):
    result = os.system(command)
    return result

avaialbleTools = {
    "cmdAgent" : {
        "fn" : cmdAgent,
        "Description" : "Runs the OS Based command"
    },
}

systemPrompt = """
You are an AI specialised system, your soul task is to resolve the user's query, from easy to complex only related to operating system command line and computer science code
also most importantly performing those command line task, depending upon the available tool
Also checking for any existing files or folders, if not found in current directory 
keep going one step backward till you reach root folder the directory.
Tha final output should be in json format.
There are few steps that you as a system need to follow:
1. Plan : Always plan or analyse the query before performing it and 
        always perform one task at a time and wait for the next input
2. Action : Perform the appropriate function from the avaialble tools.
3. Output : Provide the output in JSON format.

Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

Available tools:
    - cmdAgent : Run the OS based commands.

Example :
 User Query: What is the weather of new york?
 Output : {{"step" : "plan", "content" : "Can you provide me the current folder path"}}
 Output : {{"step" : "plan", "content" : "From the avaialble tools , I should use cmdAgent to provide you the current folder path"}}
 Output : {{"step" : "action", "function" : "cmdAgent", "input": "pwd"}}
 Output : {{"step" : "observe", "content" : "/Users/hrithik.raj/DAZN-JAVA-DEV/pythonPro/ai/ai_agent"}}
 Output : {{"step" : "output", "content" : "The current folder is : /Users/hrithik.raj/DAZN-JAVA-DEV/pythonPro/ai/ai_agents "}}
"""

messages = [{"role":"system","content" : systemPrompt}]

userQuery = input("What's your query >")
messages.append({"role": "user", "content" : userQuery})

while True:
    response  = client.chat.completions.create(
        messages = messages,
        model= "gpt-4o",
        response_format= {"type" : "json_object"}
    )
    parsedResponse = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content" : json.dumps(parsedResponse)})

    if(parsedResponse.get("step") == "plan"):
        print(f"🧠: {parsedResponse.get('content')}")
        continue
    
    if(parsedResponse.get("step") == "action"):
        toolName  = parsedResponse.get("function")
        toolCommand  = parsedResponse.get("input")

        if(avaialbleTools.get(toolName,False) != False):
            output = avaialbleTools[toolName].get('fn')(toolCommand)
            messages.append({"role" : "assistant", "content" : json.dumps({ "step": "observe", "output":  output})})
            continue

    if parsedResponse.get("step") == 'output':
        print(f"🤖: {parsedResponse.get('content')}")
        userQuery  = input("Please provide your query >")
        messages.append({"role": "user","content" : userQuery})
