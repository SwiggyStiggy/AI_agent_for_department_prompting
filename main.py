import openai
import dotenv
import os
import json

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

#this part reads my private .json files, which were exported from previously owned Microsoft teams demo environment. Afterwards adjusted by myself to my will - adding salaries or user's job experience for HR based testing.

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



#--------------------------------------------------------------------------------------



#this part basically exlpains the type of AI which will be implemented with the data mentioned above.
def generate_response(prompt_): 
    response_ = openai.ChatCompletion.create(
        model='gpt-4o-mini', #text-davinci-003  gpt-3.5-turbo gpt-4o-mini - old one if anything use this. 
        messages=conversation_history,  #!conversation_history - for chatting.    OR  ![{"role": "user", "content": prompt_}] - for single call.
        max_tokens=16384, #needs to be 100
        n=1,
        stop=None,
    )
    answer = response_.choices[0].message['content'].strip()
    return answer



#--------------------------------------------------------------------------------------


#This part defines, if you'd like the refined AI to have only single call - "single action" - this type has no memory so asking a single question returns its answer and conversation closes. "Ping-ping" on the otherhand is chat-based system,
#memorizes the conversation but drains the API token usage. In my case, single call is commented and chat-based active.

"""NECESSARY ADDITION FOR Chat-based SYSTEM________________________________NOT FOR SINGLE CALL"""

conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]


"""____________________________________"""



#SINGLE-ACTION(single call)

#while True:
#    user_question = input("Ask a question: ")
#    prompt = user_question + " " + json.dumps(data, indent=4)
#    response = generate_response(prompt)
#    print("ChatGPT: " + response)


#PING-PONG(chat-based)

while True:
    #begin conversation:
    user_question = input("Ask a question: ")
    conversation_history.append({"role": "user", "content": user_question})
    prompt_data = json.dumps(data, indent=4)
    #create temporary memory for "ping pong" chat to exist in the system"
    conversation_history.append({"role": "system", "content": f"Data available: {prompt_data}"})
    response = generate_response(conversation_history)
    print("ChatGPT: " + response)
    conversation_history.append({"role": "assistant", "content": response})

    #keeps the loop until user is done with talking with the AI.
    satisfied = input("Shall we resume the conversation? (yes/no): ").strip().lower()
    
    if satisfied == "no":
        print("Great! Ending the conversation.")
        break
    elif satisfied == "yes":
        print("Okay, let's continue the conversation.")

    else:
        print("""Please answer only with "yes" or "no", thank you!""")