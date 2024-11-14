import openai
import dotenv
import os
import json

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# these are my private .json files. Feel free to manipulate any personal data with this code.

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
        messages=conversation_history,  #conversation_history - for chatting.   [{"role": "user", "content": prompt_}] - for single call.
        max_tokens=16384, #needs to be 100
        n=1,
        stop=None,
    )
    answer = response_.choices[0].message['content'].strip()
    return answer

"""NECESSARY ADDITION FOR CHAT SYSTEM________________________________"""

# Store the conversation history
conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]  # Add a system message to set the context
"""____________________________________"""



"""Single call will be commented. Chat-type remains."""

#while True:
#    user_question = input("Ask a question: ")
#    prompt = user_question + " " + json.dumps(data, indent=4)
#    response = generate_response(prompt)
#    print("ChatGPT: " + response)

while True:
    # Ask the user for input
    user_question = input("Ask a question: ")

    # Add the user's question to the conversation history
    conversation_history.append({"role": "user", "content": user_question})

    # Append data (this could be adjusted to only append relevant data to keep prompt size smaller)
    prompt_data = json.dumps(data, indent=4)
    conversation_history.append({"role": "system", "content": f"Data available: {prompt_data}"})

    # Generate response based on the conversation history
    response = generate_response(conversation_history)

    # Show the response from the model
    print("ChatGPT: " + response)

    # Add the response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})

    # Ask the user if they are satisfied with the answer
    satisfied = input("Are you satisfied with the answer? (yes/no): ").strip().lower()
    
    if satisfied == "yes":
        print("Great! Ending the conversation.")
        break  # Exit the loop if the user is satisfied
    else:
        print("Okay, let's continue the conversation.")
        # The loop continues, and the model retains the conversation history
