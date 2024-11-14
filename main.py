import openai
import dotenv
import os
import json

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# these are my private .json files, you can use any other .json files

with open('./team_info.json') as json_file:
    team_data = json.load(json_file)

with open('./user_info.json') as json_file:
    user_data = json.load(json_file)

with open('./combined_info.json') as json_file:
    combined_data = json.load(json_file)

data = {
    "team_info": team_data,
    "user_info": user_data,
    "combined_info": combined_data
}

# -----------------------

def generate_response(prompt_): 
    response_ = openai.ChatCompletion.create(
        model='gpt-4o-mini', #text-davinci-003  gpt-3.5-turbo gpt-4o-mini - old one if anything use this. 
        messages=[{"role": "user", "content": prompt_}
                  ],
        max_tokens=16384, #needs to be 100
        n=1,
        stop=None,
    )
    answer = response_.choices[0].message['content'].strip()
    return answer


while True:
    user_question = input("Ask a question: ")
    prompt = user_question + " " + json.dumps(data, indent=4)
    response = generate_response(prompt)
    print("ChatGPT: " + response)

