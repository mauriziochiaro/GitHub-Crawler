"""
chat_manager.py: Chat management module for the GitHub Crawler Chatbot.

This module is responsible for maintaining details about the current GitHub repository being analyzed.
It serves as a central point for storing and accessing chat and repository information.
"""

########################################################################################################################

repo_owner = ""
repo_name = ""

def set_repo_details(owner, name):
    global repo_owner, repo_name
    repo_owner = owner
    repo_name = name

def get_repo_details():
    return repo_owner, repo_name
