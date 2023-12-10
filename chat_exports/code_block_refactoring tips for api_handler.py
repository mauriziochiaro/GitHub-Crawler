def append_to_chat_history(chat_history, role, content):
    chat_history.append({"role": role, "content": content})

def process_tool_calls(tool_calls):
    results = {}
    for tool_call in tool_calls:
        if tool_call.function.name == "crawl_github":
            crawl_result = crawl_github(tool_call.function.arguments.get("repo_url"))
            results[tool_call.id] = {
                "name": "crawl_github",
                "content": crawl_result
            }
    return results

def create_openai_chat_completion(user_input):
    truncate_chat_history(chat_history)
    response = client.chat.completions.create(
        model=MODEL,
        messages=chat_history,
        tools=tools,
        tool_choice="auto"
    )
    return response.choices[0].message

def fetch_openai_response_with_function_calling(user_input):
    append_to_chat_history(chat_history, "user", user_input)
    
    response_message = create_openai_chat_completion(user_input)
    
    if response_message.tool_calls:
        tool_results = process_tool_calls(response_message.tool_calls)
        for tool_id, result in tool_results.items():
            append_to_chat_history(chat_history, "tool", result['content'])

        # Fetch next response after processing the tool call
        next_response_message = create_openai_chat_completion(user_input)
        append_to_chat_history(chat_history, "assistant", next_response_message.content)
        return next_response_message.content
    else:
        append_to_chat_history(chat_history, "assistant", response_message.content)
        return response_message.content