from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()
apiKey = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=apiKey)


def getWeather(city) :
    print("🔨 Tool Called: get_weather", city)
    url = f"https://wttr.in/{city}?format=%C+%t"

    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

def findAverageWeather(temps=[]):
    print("🔨 Tool Called: findAverage Weather", temps)
    temp = 0
    for t in temps:
        temp+=t
    averageTemp  =  temp/len(temps)
    return f"The average weather of the mentioned cities is {averageTemp}"


systemPropmt =  """
You are an AI specialised system, and you are supposed to resolve the user's queries with best possible ouput.
Before reaching out to any output, you will go through the set of available tools, pick the best tool which is suitable
to resolve the user's queries.You need to wait for the observation and depending upon you need to pick the best tool
apply it give the result.

Rules:
    - Follow the output in json format
    - Always perform one task at a time and wait for the next input
    - Carefully analyse the query

Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}
Available tools:
    - getWeather : Takes city as parameter and gives the temprature as output.
    - findAverageWeather : Takes array of tempratures , find the average and give the output.

Example :
 User Query: What is the weather of new york?
 Output : {{"step" : "plan", "content" : "The user is interested in knowing the temprature of the New York"}}
 Output : {{"step" : "plan", "content" : "From the avaialble tools , I should use getWaether function to provide the temprature of New York"}}
 Output : {{"step" : "action", "function" : "getWeather", "input" : "NewYork"}}
 Output : {{"step" : "observe", "content" : "12 Degree Celsius"}}
 Output : {{"step" : "output", "content" : "The weather for new york seems to be 12 degrees."}}
"""

avaialbleTools = {
    "getWeather" : {
        "fn" : getWeather,
        "Description" : " Takes city as parameter and gives the temprature as output."
    },
    "findAverageWeather" : {
        "fn" : findAverageWeather,
        "Description" : "Takes array of tempratures , find the average and give the output."
    }
}




messages = [{"role" : "system", "content" : systemPropmt}]

userQuery  = input("Please provide your query >")
messages.append({"role": "user","content" : userQuery})

while True:
    response  = client.chat.completions.create(
        model= "gpt-4o",
        messages= messages,
        response_format= {"type" : "json_object"},
    )
    parsedResponse = json.loads(response.choices[0].message.content)
    messages.append({"role" : "assistant", "content" : json.dumps(parsedResponse)})

    if parsedResponse.get("step") == "plan":
        print(f"🧠: {parsedResponse.get('content')}")
        continue
    
    if parsedResponse.get("step") == "action":
        toolName  = parsedResponse.get("function")
        toolParameter = parsedResponse.get("input")

        if avaialbleTools.get(toolName,False) != False:
            output = avaialbleTools[toolName].get("fn")(toolParameter)
            messages.append({"role" : "assistant", "content" : json.dumps({ "step": "observe", "output":  output})})
            continue

    if parsedResponse.get("step") == 'output':
        print(f"🤖: {parsedResponse.get('content')}")
        userQuery  = input("Please provide your query >")
        messages.append({"role": "user","content" : userQuery})