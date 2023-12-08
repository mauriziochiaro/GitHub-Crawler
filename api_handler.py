"""
api_handler.py: API handling module for the GitHub Crawler Chatbot.

This module manages the interactions with external APIs, including the GitHub API and OpenAI's GPT model.
It processes user inputs, fetches data from GitHub, generates responses using the GPT model, and maintains
the conversation history.
"""

from config import MODEL, headers
import json
import requests
from openai import OpenAI
from config import OPENAI_API_KEY, MAX_TOKENS
import tiktoken
from chat_manager import set_repo_details

########################################################################################################################

# Initialize conversation history
chat_history = [{"role": "system", "content": "You are a helpful assistant named GitHub Crawler GPT. GitHub Crawler GPT specializes in analyzing GitHub projects, their codebase, and architecture. It offers practical code snippets and suggestions for practical improvements to projects. This AI tool can delve into various aspects of a project, including code quality, structure, documentation, and overall design. It provides insights and recommendations to enhance code efficiency, readability, and maintainability.\n\nIt can crawl any repository by calling one function: <crawl_github>. This function will use GitHub API for fetching and scraping repositories. <crawl_github> will be able to gather <repo_owner>, <repo_name> and <file_path> from the <repo_url>.\n\nGuidelines:\n -Always answer in markdown;\n - never ask the user to provide code from th repository, once you have the URL of the repository you can crawl every file by passing the corresponding <repo_url> directory to the <crawl_github> function."}]

client = OpenAI(api_key = OPENAI_API_KEY)

def truncate_chat_history(chat_history):
    """
    Truncate the content of messages in chat_history to fit within the specified maximum number of tokens.
    """
    encoding = tiktoken.encoding_for_model(MODEL)  # Change the encoding based on the model you're using
    total_tokens = 0
    max_tokens = MAX_TOKENS  # Adjust as per the model's limit

    for message in chat_history:
        if total_tokens >= max_tokens:
            break

        content = get_message_content(message)
        tokenized_content = encoding.encode(content)
        token_count = len(tokenized_content)

        if total_tokens + token_count > max_tokens:
            # Calculate how many tokens to keep
            tokens_to_keep = max_tokens - total_tokens
            truncated_content = encoding.decode(tokenized_content[:tokens_to_keep])
            set_message_content(message, truncated_content)

        total_tokens += len(tokenized_content)

def get_message_content(message):
    """
    Extract content from a message, whether it's a dictionary or a ChatCompletionMessage object.
    """
    if isinstance(message, dict):
        return message.get("content", "")
    elif hasattr(message, "content") and message.content:
        return message.content
    return ""

def set_message_content(message, content):
    """
    Set the content of a message.
    """
    if isinstance(message, dict):
        message["content"] = content
    elif hasattr(message, "content"):
        message.content = content

# Custom function to crawl GitHub
def crawl_github(repo_url):
    # Logic for crawling a GitHub repository
    return fetch_file_via_api(repo_url)

# Using the correct method for Chat Completions API
def fetch_openai_response_with_function_calling(user_input):
    global chat_history
    chat_history.append({"role": "user", "content": user_input})

    # Define available functions for the model to call
    tools = [
        {
            "type": "function",
            "function": {
                "name": "crawl_github",
                "description": "Crawl a GitHub repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_url": {"type": "string"}
                    },
                    "required": ["repo_url"]
                }
            }
        }
    ]

    
    truncate_chat_history(chat_history)

    # API call with function calling
    response = client.chat.completions.create(
        model=MODEL,
        messages=chat_history,
        tools=tools, 
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    # Check if a function was called
    tool_calls = response_message.tool_calls
    if tool_calls:
        chat_history.append(response_message)
        # Execute the requested function and append its result to the chat history
        for tool_call in tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "crawl_github":
                crawl_result = crawl_github(function_args.get("repo_url"))
                chat_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "crawl_github",
                    "content": crawl_result
                })

        truncate_chat_history(chat_history)
        # Get the next response from the model
        next_response = client.chat.completions.create(
            model=MODEL, 
            messages=chat_history
        )
        next_assistant_message = next_response.choices[0].message
        chat_history.append({"role": "assistant", "content": next_assistant_message.content})

        return next_assistant_message.content
    else:
        # If no function was called, simply append the assistant's response and return it
        chat_history.append({"role": "assistant", "content": response_message.content})
        return response_message.content
    
def fetch_directory_contents(api_url):
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve content from {api_url} with status code:", response.status_code)
        return []

    contents = response.json()
    directory_items = []

    for item in contents:
        if item['type'] == 'dir':
            # If the item is a directory, recursively fetch its contents
            directory_items.append(f"Directory: {item['name']}")
            nested_items = fetch_directory_contents(item['url'])
            directory_items.extend(['\t' + nested_item for nested_item in nested_items])
        else:
            # If the item is a file, add its path to the list
            directory_items.append(f"File: {item['name']} ({item['html_url']})")

    return directory_items

def fetch_file_via_api(repo_url):
    try:
        # Split the URL to get the necessary parts
        parts = repo_url.replace("https://github.com/", "").split("/")
        repo_owner, repo_name = parts[0], parts[1]

        # Construct the API URL
        if len(parts) <= 2:
            api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"
        else:
            if 'blob' in parts:
                file_path_parts = parts[parts.index('blob') + 2:]
                file_path = '/'.join(file_path_parts)
                api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
            else:
                return "Invalid URL format."
            
        set_repo_details(repo_owner, repo_name)  

        # Include the access token in the request header for authentication
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            if isinstance(json_data, list):
                # List the contents of the directory, including nested items
                directory_contents = fetch_directory_contents(api_url)
                return "\n".join(directory_contents)
            elif 'download_url' in json_data:
                # If it's a file, return its content
                file_content = requests.get(json_data['download_url']).text
                return file_content
            else:
                return "Non-text file content cannot be displayed."
        else:
            error_message = f"Failed to retrieve content from {api_url} with status code: {response.status_code}"
            print(error_message)
            return error_message
    except Exception as e:
        error_message = f"An error occurred while processing the request: {str(e)}"
        print(error_message)
        return error_message
