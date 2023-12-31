"""
gui.py: Graphical User Interface (GUI) module for the GitHub Crawler Chatbot.

This module contains functions and configurations related to the chatbot's GUI,
such as sending messages, updating the chat display, and saving chat history. It defines
the visual elements and their behavior within the chat interface.
"""

import tkinter as tk
from api_handler import fetch_openai_response_with_function_calling
from datetime import datetime
from tkinter import filedialog
from chat_manager import get_repo_details
import os

########################################################################################################################

def save_chat_as_markdown(chat_display, parent_window):
    repo_owner, repo_name = get_repo_details()
    chat_text = chat_display.get("1.0", tk.END)
    # markdown_text = convert_text_to_markdown(chat_text)

    suggested_filename = f"{repo_owner}-{repo_name}.md" if repo_owner and repo_name else "chat_history.md"
    export_folder = "chat_exports"  # Name of the subfolder

    # Ensure the export folder exists
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Set the full path including the subfolder
    initialdir = os.path.join(os.getcwd(), export_folder)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".md",
        filetypes=[("Markdown files", "*.md")],
        parent=parent_window,
        title="Save Chat History",
        initialdir=initialdir,  # Set initial directory to the export folder
        initialfile=suggested_filename
    )
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(chat_text)
      
def send_user_message(user_input_field, chat_display):
    # Get user input from the input field
    user_input = user_input_field.get().strip()

    # Input validation: Check if the user input is not empty
    if not user_input:
        # Display an error message to the user
        display_error_message(chat_display, "Please enter a valid message.")
        return

    # Display the user's input in the chat display
    update_chat_display('You', user_input, chat_display)

    try:
        # Get the AI response based on the user input
        ai_response = fetch_openai_response_with_function_calling(user_input)
        # Display the AI response in the chat display
        update_chat_display('Assistant', ai_response, chat_display)
    except Exception as e:
        # Handle any errors that occur during the AI response retrieval
        display_error_message(chat_display, f"An error occurred: {str(e)}")
    finally:
        # Clear the user input field after processing
        user_input_field.delete(0, tk.END)

def display_error_message(chat_display, error_message):
    """
    Display an error message in the chat display.
    """
    # Add error message to the chat display with a distinct style
    update_chat_display('Error', error_message, chat_display)

def update_chat_display(sender, message, chat_display):
    timestamp = datetime.now().strftime("%H:%M:%S")
    chat_display.config(state=tk.NORMAL)

    if sender == 'You':
        sender_emoji = "🤓 YOU"  # Emoji for the user
    else:
        sender_emoji = "🕷️ CRAWLER"  # Emoji for the assistant

    formatted_message = f"\n{timestamp} {sender_emoji}\n\n"
    chat_display.insert(tk.END, formatted_message)
    add_markdown_text(message, chat_display)
    chat_display.insert(tk.END, "-"*50 + "\n", 'separator')  # Separator line
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)

def add_markdown_text(text, chat_display):
    lines = text.split('\n')
    code_block = False  # To track whether we're inside a code block

    for line in lines:
        if line.startswith('#### '):
            chat_display.insert(tk.END, line[5:] + '\n', 'header4')
        elif line.startswith('### '):
            chat_display.insert(tk.END, line[4:] + '\n', 'header3')  
        elif line.startswith('## '):
            chat_display.insert(tk.END, line[3:] + '\n', 'header2')               
        elif line.startswith('```'):
            code_block = not code_block
            continue  # Skip the delimiter line
        elif code_block:
            if line.strip().startswith('# ') or line.strip().startswith('// '):
                # Style comment lines inside code blocks differently
                chat_display.insert(tk.END, line + '\n', 'comment')
            else:
                chat_display.insert(tk.END, line + '\n', 'code')
        else:
            chat_display.insert(tk.END, line + '\n', 'normal')



