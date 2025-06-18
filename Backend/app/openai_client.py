from .client import client
from .functions import submit_business_details , customize_css
from datetime import datetime
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, '..', 'data', 'prompt.txt')

PROMPT = ""

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    PROMPT = f.read()

# ----------------------------
# SYSTEM PROMPT
# ----------------------------
SYSTEM_PROMPT = PROMPT


# ----------------------------
# FUNCTION DEFINITIONS (TOOLS)
# ----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "submitBusinessDetails",
            "description": "Submit the user's business category once available. Business category must exactly match one of the known categories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_category": {
                        "type": "string",
                        "description": "Type of business.Strictly return a category from any of the following : Grocery , Shopping"
                    }
                },
                "required": ["business_category"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "customizeCSS",
        "description": "Customize a part of the selected theme's CSS file.",
        "parameters": {
            "type": "object",
            "properties": {
                "property_to_change": {
                    "type": "string",
                    "description": "The part of the theme to modify, like button color, text size, background, etc."
                },
                "new_value": {
                    "type": "string",
                    "description": "The new value the user wants, e.g., 'red', '18px', '#000', etc."
                }
            },
            "required": ["property_to_change", "new_value"]
        }
    }
}

]

def sanitize_chat_history(chat_history):
    for message in chat_history:
        # Fix tool message content if it's a dict
        if message["role"] == "tool" and isinstance(message.get("content"), dict):
            message["content"] = json.dumps(message["content"])
    return chat_history

# ----------------------------
# OPENAI CHAT FUNCTION
# ----------------------------
def get_openai_response(user_input, chat_history):
    try:
        # Add system prompt if not yet present
        if not any(msg['role'] == 'system' for msg in chat_history):
            chat_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

        # Add user input to history
        chat_history.append({"timestamp": datetime.now().isoformat() , "role": "user", "content": user_input})

        sanitized_history = sanitize_chat_history(chat_history)

        # Send to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-theme-customization",
            messages=sanitized_history,
            tools=tools,
            tool_choice="auto"
        )

        choice = response.choices[0]
        message = choice.message

        if message.tool_calls:
            assistant_timestamp = datetime.now().isoformat()
            chat_history.append({
                "timestamp": assistant_timestamp,
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        },
                        "type": tc.type
                    }
                    for tc in message.tool_calls
                ]
            })

            tool_call = message.tool_calls[0].model_dump()
            function_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])


            # Call the appropriate function
            if function_name == "submitBusinessDetails":
                valid_categories = [
                                    "pharmacy","general store","fruits & vegetables","meat shop","bakery shop","mobile store",
                                    "electronics shop","restaurant","book shop","beauty store","clothing store","gift shop","hardware shop",
                                    "service & repair","saloon shop","computer & accessories shop","home & kitchen appliance","photostat & telecom","watch store","shopping"
                                    ]   
                category = arguments.get("business_category", "").strip().lower()

                if category in [vc.lower() for vc in valid_categories]:
                    
                    themes  = submit_business_details(**arguments)
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "reply" : "Please select a theme!", 
                        "themes" : themes
                    }
                else:
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "error": f"'{category}' is not a valid business category. Please choose from: {', '.join(valid_categories)}"
                    }
            elif function_name == "customizeCSS":
                css_result = customize_css(**arguments)
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "css" : css_result
                }

            else:
                result = {
                    "timestamp": datetime.now().isoformat(),
                    "error": f"Unknown function: {function_name}"
                }

            chat_history.append({
                "timestamp": datetime.now().isoformat(),
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": result
            })


            return result

        else:
            timestamp = datetime.now().isoformat()
            chat_history.append({"timestamp": timestamp ,"role": "assistant", "content": message.content})
            return {"timestamp" : timestamp , "content" : message.content }

    except Exception as e:
        return f"Error: {str(e)}"