import tkinter as tk
from tkinter import scrolledtext
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


def ask_question():
    question = question_entry.get()
    prompt = question + " " + json.dumps(data)
    response = generate_response(prompt)
    response_text.insert(tk.END, "User: " + question + "\n")
    response_text.insert(tk.END, "ChatGPT: " + response + "\n")
    response_text.insert(tk.END, "\n")
    question_entry.delete(0, tk.END)


# Create the main window
window = tk.Tk()
window.title("ChatGPT GUI")

# Create the question entry widget
question_entry = tk.Entry(window, width=50)
question_entry.pack(pady=10)

# Create the "Ask" button
ask_button = tk.Button(window, text="Ask", command=ask_question)
ask_button.pack(pady=5)

# Create the response text widget
response_text = scrolledtext.ScrolledText(window, width=60, height=20)
response_text.pack(pady=10)

# Start the GUI event loop
window.mainloop()