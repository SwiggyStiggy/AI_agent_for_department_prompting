import openai
import dotenv
import os
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon


dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

with open('./department_info.json') as json_file:
    department_data = json.load(json_file)

with open('./user_info.json') as json_file:
    user_data = json.load(json_file)

with open('./CV_info.json') as json_file:
    cv_info = json.load(json_file)

with open('./projects_info.json') as json_file:
    projects_info = json.load(json_file)

with open('./client_info.json') as json_file:
    clients_info = json.load(json_file)

with open('./finance_info.json') as json_file:
    finance_info = json.load(json_file)

with open('./permissions.json') as json_file:
    permissions = json.load(json_file)

    
data = {
    "department_info": department_data,
    "user_info": user_data,
    "cv_info": cv_info,
    "projects_info": projects_info,
    "clients_info": clients_info,
    "finance_info.json": finance_info,
}

def get_user_role(user_id):
    # Find the user's role from user_info.json
    for user in user_data:
        if user["User Id"] == user_id:
            return user["Role"]
    return None  # Default to no role if user is not found


def filter_data_by_role(role):
    # Filter data based on the user's role
    accessible_data = {}
    if role in permissions:
        allowed_files = permissions[role]["allowed_files"]
        for file in allowed_files:
            if file in data:
                accessible_data[file] = data[file]
    return accessible_data


def generate_response(conversation_history): 
    response_ = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=conversation_history,
        max_tokens=1000,
        temperature=0.7,
        n=1
    )
    answer = response_.choices[0].message.content.strip()
    return answer


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CoreTEX Chatbot')
        self.setGeometry(100, 100, 600, 400)

        self.setWindowIcon(QIcon('logo.png')) #logo

        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        
        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        #logo INSIDE the window
        logo_label = QLabel(self)
        pixmap = QPixmap('logo.png')
        logo_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_layout = QHBoxLayout()
        title_layout.addWidget(logo_label)
        title_layout.addWidget(QLabel("CoreTEX Chatbot")) 
        
        main_layout.addLayout(title_layout)

        # Chat window (Text area to display chat)
        self.chat_window = QTextEdit(self)
        self.chat_window.setReadOnly(True)
        main_layout.addWidget(self.chat_window)

        # Input field
        self.user_input = QLineEdit(self)
        self.user_input.setStyleSheet("background-color: #646464; color: white;")
        input_layout.addWidget(self.user_input)
        self.user_input.setMinimumHeight(40) 

        # Send button
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.start_conversation)
        self.send_button.setStyleSheet("background-color: #1d58eb; color: white; border-radius: 10px; padding: 10px;")
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

    def start_conversation(self):
        user_question = self.user_input.text()

        if user_question.strip() != "":  # Prevent sending empty messages
            self.conversation_history.append({"role": "user", "content": user_question})
            prompt_data = json.dumps(data, indent=4)
            self.conversation_history.append({"role": "system", "content": f"Data available: {prompt_data}"})

            response = generate_response(self.conversation_history)

            # Display user message and assistant response in chat window
            self.chat_window.append(f"You: {user_question}")
            self.chat_window.append(f"ChatGPT: {response}")

            # Append assistant's response to the conversation history
            self.conversation_history.append({"role": "assistant", "content": response})

            # Clear the input field after the message is sent
            self.user_input.clear()

    def exit_application(self):
        self.close()

    
    def keyPressEvent(self, event):
        # If Enter is pressed, trigger the send conversation function
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.start_conversation()

        # If ESC is pressed, exit the application
        if event.key() == Qt.Key.Key_Escape:
            self.exit_application()


if __name__ == '__main__':
    app = QApplication([])
    window = ChatWindow()
    window.show()
    app.exec()
