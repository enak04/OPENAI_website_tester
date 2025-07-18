from .client import client
from .functions import *
from database.modifying_databases import make_data, insert_data, retrieve_data , make_theme_data , insert_theme_data
from rapidfuzz import process

from datetime import datetime
import json
import os

# ----------------------------
# SYSTEM PROMPT SETUP
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, '..', 'static' , 'prompts', 'basic_prompt.txt')

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read() 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /Backend/app
categories_path = os.path.abspath(os.path.join(BASE_DIR, "..", 'static' , 'prompts', "categories.json")) 

def load_categoriess(path=categories_path):
    
    with open(path, "r") as file:
        return json.load(file)

def resolve_category(user_input, categories, threshold=80):

    normalized_map = {cat.lower(): cat for cat in categories}
    normalized_categories = list(normalized_map.keys())

    # Convert to lowercase for consistent matching
    user_input = user_input.lower().strip()
    match, score, _ = process.extractOne(user_input, normalized_categories)
    return normalized_map[match] if score >= threshold else None

tools = [
    {
        "type": "function",
        "function": {
            "name": "submitBusinessThemeDetails",
            "description": "Submit the user's business category and preferred template colors. If a template has already been given before and user doesn't want a new template DO NOT CALL THIS TOOL",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_category": {
                        "type": "string",
                        "description": "The user's business category (must match allowed list)." , 
                        "enum": [
                            "Pharmacy",
                            "General Store",
                            "Fruits & Vegetables",
                            "Meat Shop",
                            "Bakery Shop",
                            "Mobile Store",
                            "Electronics Shop",
                            "Restaurant",
                            "Book Shop",
                            "Beauty Store",
                            "Clothing Store",
                            "Gift Shop",
                            "Hardware Shop",
                            "Service & Repair",
                            "Saloon Shop",
                            "Computer & Accessories Shop",
                            "Home & Kitchen Appliance",
                            "Photostat & Telecom",
                            "Watch Store",
                            "Fashion"
                        ]
                    },
                    "primary_color": {
                        "type": "string",
                        "description": "Primary color for the website theme."
                    },
                    "secondary_color": {
                        "type": "string",
                        "description": "Secondary color for the website theme."
                    }
                },
                "required": ["business_category", "primary_color", "secondary_color"]
            }
        }
    }, 
    {
        "type" : "function",
        "function" : {
            "name": "edit_css",
            "description": "Use this when the user wants to edit their website theme’s CSS based on a prompt using AI suggestions. Only call this when you feel you have all required data. If the user’s request is too vague (e.g., ‘change the product card’), ask clarifying questions first (e.g., how many product cards, what style/colors) before calling this function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt describing what the user wants to change in their website's appearance.Keep in mind that the prompt should be such given that it does not misinterpret user's intent.DO NOT ADD YOUR OWN INFORMATION.Say for an example if the user wants to delete just the product card then don't give a prompt that deletes other sections of the website.Be smart."
                    }
                },
                "required": ["prompt"]
            }
        }
    }
]



def sanitize_chat_history(chat_history):
    for message in chat_history:
        if message["role"] == "tool" and isinstance(message.get("content"), dict):
            message["content"] = json.dumps(message["content"])
    return chat_history

def get_openai_response(user_input, chat_history, user_id, session_id , json_id):
    try:
        # Add system prompt if not present
        if not any(msg['role'] == 'system' for msg in chat_history):
            chat_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
            make_data(chat_history, user_id, session_id)

        # Add user input to chat history
        appending_chat = {
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": user_input
        }
        chat_history.append(appending_chat)
        insert_data(appending_chat, user_id, session_id)

        # Retrieve full sanitized chat history
        messages = sanitize_chat_history(retrieve_data(user_id, session_id))

        # OpenAI call
        response = client.chat.completions.create(
            model="gpt-4o-theme-customization",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature = 0.4
        )

        message = response.choices[0].message
        tool_call_results = []

        # ---------------- TOOL CALL HANDLING ----------------
        if message.tool_calls:
            tool_call_data_list = [call.model_dump() for call in message.tool_calls]

            # Add assistant's tool call message (don't json.dumps here)
            assistant_tool_call_msg = {
                "timestamp": datetime.now().isoformat(),
                "role": "assistant",
                "tool_calls": tool_call_data_list,
                "content": None
            }
            chat_history.append(assistant_tool_call_msg)
            insert_data(assistant_tool_call_msg, user_id, session_id)

            for tool_call_data in tool_call_data_list:
                function_name = tool_call_data["function"]["name"]
                arguments = json.loads(tool_call_data["function"]["arguments"])
                tool_call_id = tool_call_data["id"]

                if function_name == "submitBusinessThemeDetails":
                

                    theme_result = submit_business_theme_details(
                        business_category=arguments["business_category"],
                        primary_color=arguments["primary_color"],
                        secondary_color=arguments["secondary_color"],
                        chat_history=chat_history
                    )

                    

                    if isinstance(theme_result, dict):
                        result = {
                            "timestamp": datetime.now().isoformat(),
                            **theme_result
                        }
                    else:
                        result = {
                            "timestamp": datetime.now().isoformat(),
                            "theme": theme_result
                        }

                    # Add tool result message (store dict, not json string)
                    tool_msg = {
                        "timestamp": datetime.now().isoformat(),
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "name": function_name,
                        "content": result  # ✅ keep as dict
                    }
                    chat_history.append(tool_msg)
                    insert_data(tool_msg, user_id, session_id)

                    # Save theme CSS
                    # css_to_add = get_theme("hi")
                    # make_theme_data(css_to_add, user_id, session_id)
                    # chat_history.append(tool_msg)
                    # insert_data(tool_msg, user_id, session_id)

                    tool_call_results.append(result)


                elif function_name == "edit_css":
                    print("Edit_css is being called")
                    css_result = edit_css(**arguments , user_id = user_id , json_id = json_id)
                    result = {
                            "timestamp": datetime.now().isoformat(),
                            **css_result
                        }
                    tool_msg = {
                        "timestamp": datetime.now().isoformat(),
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "name": function_name,
                        "content": css_result  # ✅ keep as dict
                    }
                    
                    chat_history.append(tool_msg)
                    insert_data(tool_msg, user_id, session_id)
                    tool_call_results.append(result)

            
            return tool_call_results  # ✅ return all tool responses

        # ---------------- NO TOOL CALL CASE ----------------
        else:
            timestamp = datetime.now().isoformat()
            assistant_msg = {
                "timestamp": timestamp,
                "role": "assistant",
                "content": message.content
            }
            chat_history.append(assistant_msg)
            insert_data(assistant_msg, user_id, session_id)
            return {"timestamp": timestamp, "content": message.content}

    except Exception as e:
        return {"error": str(e)}
