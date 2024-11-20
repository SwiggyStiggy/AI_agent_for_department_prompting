import openai
import dotenv
import os
import json
import tkinter as tk

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

with open('./team_info.json') as json_file:
    team_data = json.load(json_file)                     #List of existing teams inside the company.

with open('./user_info.json') as json_file:
    user_data = json.load(json_file)                     #List of existing users inside the company.

with open('./CV_info.json') as json_file:
    cv_info = json.load(json_file)                       #List of previously received CVs for our HR Department.

with open('./projects_info.json') as json_file:
    projects_info = json.load(json_file)                 #List of projects for Development Team.

with open('./client_info.json') as json_file:
    clients_info = json.load(json_file)                  #List of clients for our Sales Team.

data = {
    "team_info": team_data,
    "user_info": user_data,
    "cv_info": cv_info,
    "projects_info": projects_info,
    "clients_info": clients_info
}



#--------------------------------------------------------------------------------------



def generate_response(conversation_history): 
    response_ = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=conversation_history,
        max_tokens=1640,
        temperature=0.7,
        n=1
    )
    answer = response_.choices[0].message.content.strip()
    return answer


def start_conversation(event=None):
    user_question = user_input.get()
    
    if user_question.strip() != "":  # Prevent sending empty messages
        conversation_history.append({"role": "user", "content": user_question})
        prompt_data = json.dumps(data, indent=4)
        conversation_history.append({"role": "system", "content": f"Data available: {prompt_data}"})
        
        response = generate_response(conversation_history)
        
        # Display user message and assistant response in chat window
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_question + "\n")
        chat_window.insert(tk.END, "ChatGPT: " + response + "\n")
        chat_window.config(state=tk.DISABLED)
        
        # Append assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})
        
        # Clear the input field after the message is sent
        user_input.delete(0, tk.END)
        user_input.focus()

# Exit app
def exit_application(event=None):
    root.quit()

# Initialize
root = tk.Tk()
root.title("CoreTEX Chatbot")
root.configure(bg='#414141')

# Chat window
chat_window = tk.Text(root, height=20, width=100)
chat_window.pack(pady=10)
chat_window.configure(bg='#646464',fg='white')



# Input
user_input = tk.Entry(root, width=40)
user_input.pack(pady=10)
user_input.configure(bg='#646464', fg='white', insertbackground='white')


# Send button
send_button = tk.Button(root, text="Send", command=start_conversation)
send_button.pack(side='left',padx=20, pady=10)
send_button.configure(bg='#e35d5d')


# Exit Button
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack(side="right", padx=20, pady=10)
exit_button.configure(bg='#e35d5d')



#Hotkeys
user_input.bind("<Return>", start_conversation)
root.bind("<Escape>", exit_application)


conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]


root.mainloop()
