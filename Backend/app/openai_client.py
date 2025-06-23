from .client import client
from .functions import submit_business_theme_details , customize_css , submit_color_preferences , get_theme
from mongodb.modifying_databases import make_data, insert_data, retrieve_data , make_theme_data , insert_theme_data
from rapidfuzz import process

from datetime import datetime
import json
import os

# ----------------------------
# SYSTEM PROMPT SETUP
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_PATH = os.path.join(BASE_DIR, '..', 'data', 'basic_prompt.txt')

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    SYSTEM_PROMPT = f.read() 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /Backend/app
categories_path = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "categories.json")) 

def load_categoriess(path=categories_path):
    print("Error here")
    with open(path, "r") as file:
        return json.load(file)

def resolve_category(user_input, categories, threshold=80):
    # Convert to lowercase for consistent matching
    user_input = user_input.lower().strip()
    match, score, _ = process.extractOne(user_input, categories)
    return match if score >= threshold else None


# ----------------------------
# OPENAI RESPONSE HANDLER
# ----------------------------
# def get_openai_response(user_input, chat_history):
    # try:
    #     if not any(msg['role'] == 'system' for msg in chat_history):
    #         chat_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

    #     chat_history.append({
    #         "timestamp": datetime.now().isoformat(),
    #         "role": "user",
    #         "content": user_input
    #     })

    #     sanitized_history = sanitize_chat_history(chat_history)

    #     response = client.chat.completions.create(
    #         model="gpt-4o-theme-customization",
    #         messages=sanitized_history,
    #         tools=tools,
    #         tool_choice="auto"
    #     )

    #     message = response.choices[0].message
    #     tool_call_results = []

    #     if message.tool_calls:
    #         for tool_call in message.tool_calls:
    #             tool_call_data = tool_call.model_dump()
    #             function_name = tool_call_data["function"]["name"]
    #             arguments = json.loads(tool_call_data["function"]["arguments"])
    #             tool_call_id = tool_call_data["id"]

    #             if function_name == "submitBusinessDetails":
    #                 valid_categories = [
    #                     "pharmacy", "general store", "fruits & vegetables", "meat shop", "bakery shop",
    #                     "mobile store", "electronics shop", "restaurant", "book shop", "beauty store",
    #                     "clothing store", "gift shop", "hardware shop", "service & repair", "saloon shop",
    #                     "computer & accessories shop", "home & kitchen appliance", "photostat & telecom",
    #                     "watch store", "shopping", "fashion"
    #                 ]
    #                 category = arguments.get("business_category", "").strip().lower()

    #                 if category in [vc.lower() for vc in valid_categories]:
    #                     themes = submit_business_details(**arguments)
    #                     result = {
    #                         "timestamp": datetime.now().isoformat(),
    #                         "reply": "Is this theme okay for you ?",
    #                         "themes": themes
    #                     }
    #                 else:
    #                     result = {
    #                         "timestamp": datetime.now().isoformat(),
    #                         "error": f"'{category}' is not a valid business category. Please choose from: {', '.join(valid_categories)}"
    #                     }

    #             else:
    #                 result = {
    #                     "timestamp": datetime.now().isoformat(),
    #                     "error": f"Unknown function: {function_name}"
    #                 }

    #             chat_history.append({
    #                 "timestamp": datetime.now().isoformat(),
    #                 "role": "tool",
    #                 "tool_call_id": tool_call_id,
    #                 "name": function_name,
    #                 "content": result
    #             })

    #             tool_call_results.append(result)

    #         return tool_call_results

    #     else:
    #         timestamp = datetime.now().isoformat()
    #         chat_history.append({"timestamp": timestamp, "role": "assistant", "content": message.content})
    #         return {"timestamp": timestamp, "content": message.content}

    # except Exception as e:
    #     return {"error": str(e)}






# def get_openai_response(user_input, chat_history , user_id , session_id):
#     try:
#         # Add system prompt if not present
#         if not any(msg['role'] == 'system' for msg in chat_history):
#             chat_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
#             make_data(chat_history , user_id , session_id )


        
#         # Add user input
#         appending_chat = {
#             "timestamp": datetime.now().isoformat(),
#             "role": "user",
#             "content": user_input
            
#         }
#         chat_history.append(appending_chat)
        
#         # Sanitize chat history
#         sanitized_history = sanitize_chat_history(chat_history)
#         insert_data(appending_chat , user_id , session_id)

#         print(retrieve_data)

#         messages = retrieve_data(user_id , session_id)

#         # Send request to OpenAI
#         response = client.chat.completions.create(
#             model="gpt-4o-theme-customization",
#             messages=messages,
#             tools=tools,
#             tool_choice="auto"
#         )

#         message = response.choices[0].message
#         tool_call_results = []

#         # ---- TOOL CALL HANDLING ----
#         if message.tool_calls:
#             tool_call_data_list = [call.model_dump() for call in message.tool_calls]

#             # 1. Add assistant's tool call message
#             append_tool_call_message = {
#                 "timestamp": datetime.now().isoformat(),
#                 "role": "assistant",
#                 "tool_calls": tool_call_data_list,
#                 "content": None
#             }
#             chat_history.append(append_tool_call_message)
#             insert_data(append_tool_call_message , user_id , session_id)

#             for tool_call_data in tool_call_data_list:
#                 function_name = tool_call_data["function"]["name"]
#                 arguments = json.loads(tool_call_data["function"]["arguments"])
#                 tool_call_id = tool_call_data["id"]

#                 if function_name == "submitBusinessThemeDetails":
#                     theme_result = submit_business_theme_details(
#                         business_category=arguments["business_category"],
#                         primary_color=arguments["primary_color"],
#                         secondary_color=arguments["secondary_color"],
#                         chat_history=chat_history
#                     )
#                     result = {
#                         "timestamp": datetime.now().isoformat(),
#                         "theme": theme_result,
#                         "content" :"select a theme"
#                     }
#                     append_tool_call_message = {
#                         "timestamp": datetime.now().isoformat(),
#                         "role": "tool",
#                         "tool_call_id": tool_call_id,
#                         "name": function_name,
#                         "content": json.dumps(result)

#                     }
#                     chat_history.append(append_tool_call_message)
#                     insert_data(append_tool_call_message , user_id , session_id)

#                     append_tool_call_message = {
#                         "timestamp": datetime.now().isoformat(),
#                         "role": "assistant",
#                         "content": (
#                             f"Here's your theme for a **{arguments['business_category']}** website with:\n"
#                             f"🎨 Primary: **{arguments['primary_color']}**, Secondary: **{arguments['secondary_color']}**\n\n"
#                             f"Let me know if you’d like to change anything else!"
#                         )
#                     }

#                     chat_history.append(append_tool_call_message)
#                     insert_data(append_tool_call_message , user_id , session_id)
#                     css_to_add = get_theme("hi")
#                     make_theme_data(css_to_add , user_id , session_id )

#                     tool_call_results.append(result)
                        
#                 elif function_name == "customizeCSS":
#                     css_result = customize_css(**arguments , user_id = user_id , session_id = session_id)
#                     if css_result.startswith("* {"):
#                         result = {
#                             "timestamp": datetime.now().isoformat(),
#                             "css": css_result,
#                             "role" : "assistant"
#                         }
#                     else:
#                         result = {
#                             "timestamp": datetime.now().isoformat(),
#                             "content": css_result,
#                             "role" : "assistant"
#                         }
#                     chat_history.append(result)
#                     insert_data(result , user_id , session_id)
#                     insert_theme_data(css_result , user_id , session_id)
#                     tool_call_results.append(result)
#             return result

#         # ---- NO TOOL CALL ----
#         else:
#             timestamp = datetime.now().isoformat()
#             append_message = {
#                 "timestamp": timestamp,
#                 "role": "assistant",
#                 "content": message.content
#             }
#             chat_history.append(append_message)
#             insert_data(append_message , user_id , session_id)
#             return {"timestamp": timestamp, "content": message.content}

#     except Exception as e:
#         return {"error": str(e)}

# ----------------------------
# FUNCTION DEFINITIONS (TOOLS)
# ----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "submitBusinessThemeDetails",
            "description": "Submit the user's business category and preferred theme colors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_category": {
                        "type": "string",
                        "description": "The user's business category (must match allowed list)."
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
        "type": "function",
        "function": {
            "name": "customizeCSS",
            "description": "Customize part of the selected theme's CSS.",
            "parameters": {
                "type": "object",
                "properties": {
                    "property_to_change": {
                        "type": "string",
                        "description": "The CSS property to change (e.g., background color)."
                    },
                    "new_value": {
                        "type": "string",
                        "description": "The new value for the CSS property (e.g., 'red')."
                    }
                },
                "required": ["property_to_change", "new_value"]
            }
        }
    }
]

# ----------------------------
# CHAT HISTORY CLEANUP
# ----------------------------
# def sanitize_chat_history(chat_history):
#     for message in chat_history:
#         if message["role"] == "tool" and isinstance(message.get("content"), dict):
#             message["content"] = json.dumps(message["content"])
#     return chat_history



def sanitize_chat_history(chat_history):
    for message in chat_history:
        if message["role"] == "tool" and isinstance(message.get("content"), dict):
            message["content"] = json.dumps(message["content"])
    return chat_history

def get_openai_response(user_input, chat_history, user_id, session_id):
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
            tool_choice="auto"
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
                    categories = load_categoriess()
                    input_category = arguments["business_category"]
                    fuzzymatchedbusiness_category = resolve_category( input_category, categories)
                    print("Error here")

                    theme_result = submit_business_theme_details(
                        business_category=fuzzymatchedbusiness_category,
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

                    # Add assistant confirmation message
                    assistant_msg = {
                        "timestamp": datetime.now().isoformat(),
                        "role": "assistant",
                        "content": (
                            f"Here's your theme for a **{arguments['business_category']}** website with:\n"
                            f"🎨 Primary: **{arguments['primary_color']}**, Secondary: **{arguments['secondary_color']}**\n\n"
                            f"Let me know if you’d like to change anything else!"
                        )
                    }
                    chat_history.append(assistant_msg)
                    insert_data(assistant_msg, user_id, session_id)

                    # Save theme CSS
                    css_to_add = get_theme("hi")
                    make_theme_data(css_to_add, user_id, session_id)

                    tool_call_results.append(result)

                elif function_name == "customizeCSS":
                    css_result = customize_css(**arguments, user_id=user_id, session_id=session_id)

                    css_msg = {
                        "timestamp": datetime.now().isoformat(),
                        "role": "assistant",
                        "content": css_result if not css_result.startswith("* {") else None,
                        "css": css_result if css_result.startswith("* {") else None
                    }

                    chat_history.append(css_msg)
                    insert_data(css_msg, user_id, session_id)

                    if css_result.startswith("* {"):
                        insert_theme_data(css_result, user_id, session_id)

                    tool_call_results.append(css_msg)

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
