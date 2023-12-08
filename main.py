"""
main.py: Main module of the GitHub Crawler Chatbot application.

This module initializes the application's graphical user interface and ties together
the functionalities provided by other modules. It sets up the layout and appearance
of the chat interface, manages user interactions, and invokes the chatbot's core functionalities.
"""

from tkinter import ttk, font
import tkinter as tk
from gui import send_user_message, save_chat_as_markdown

########################################################################################################################

root = tk.Tk()
root.title("Provide URL of a Repo and Chat with GitHub Crawler")
root.geometry('1200x1000')

style = ttk.Style(root)
style.theme_use('clam')

# Chat display area
chat_frame = tk.Frame(root)
chat_display = tk.Text(chat_frame, state=tk.DISABLED, padx=10, pady=10)  # Adding padding
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(chat_frame, command=chat_display.yview)
chat_display['yscrollcommand'] = scrollbar.set
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Define fonts and styles
header4_font = font.Font(family="monospace", size=10, weight="bold")
header3_font = font.Font(family="monospace", size=12, weight="bold")
header2_font = font.Font(family="monospace", size=10, weight="bold")

# Define a different style for code blocks
code_font = font.Font(family="monospace", size=10)
chat_display.tag_configure('header4', font=header4_font)
chat_display.tag_configure('header3', font=header3_font)
chat_display.tag_configure('header2', font=header2_font)
# Define styles for code blocks (dark mode) and comments
chat_display.tag_configure('code', font=code_font, background="#333333", foreground="#ffffff")  # Dark background, light text
chat_display.tag_configure('comment', background="#333333", foreground="#90ee90")  # Dark green text for comments
chat_display.tag_configure('normal', font=code_font)

# User input and Send button area
input_frame = tk.Frame(root)
user_input_field = ttk.Entry(input_frame, width=40)
user_input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
user_input_field.bind("<Return>", lambda event: send_user_message(user_input_field, chat_display))

send_button = ttk.Button(input_frame, text="Send", command=lambda: send_user_message(user_input_field, chat_display))

send_button.pack(side=tk.LEFT)
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Download button
download_button = ttk.Button(input_frame, text="Download", command=lambda: save_chat_as_markdown(chat_display, root))
download_button.pack(side=tk.RIGHT)

if __name__ == "__main__":
    root.mainloop()
