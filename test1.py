import openai
import dotenv
import os
import json

dotenv.load_dotenv('.env')
API_AI = os.getenv('API_AI')
openai.api_key = API_AI

# Load JSON data
with open('team_info.json') as json_file:
    team_data = json.load(json_file)

with open('user_info.json') as json_file:
    user_data = json.load(json_file)

data = team_data = user_data


def generate_response(prompt_):
    response_ = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt_,
        max_tokens=100,
        n=1,
        stop=None,
    )
    answer = response_.choices[0].text.strip()
    return answer
