import tkinter as tk
from tkinter import scrolledtext
import json
from main import generate_response, data

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