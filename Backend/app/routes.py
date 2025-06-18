from flask import Blueprint, request, jsonify
from .openai_client import get_openai_response
import re
import os
import json

HISTORY_DIR = "chat_histories"

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)


def is_probably_css(text):
    """Simple heuristic to check if the content looks like CSS."""
    return bool(re.search(r'\b(?:color|background|font|padding|margin|border)\b\s*:', text))

def get_history_file_path(user_id):
    return os.path.join(HISTORY_DIR, f"{user_id}.json")

def load_chat_history(user_id):
    path = get_history_file_path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# def save_chat_history(user_id, chat_history):
#     path = get_history_file_path(user_id)

#     serializable_history = []

#     for msg in chat_history:
#         msg_copy = msg.copy()

#         # Handle assistant tool_calls
#         if "tool_calls" in msg_copy and isinstance(msg_copy["tool_calls"], list):
#             serialized_tool_calls = []

#             for call in msg_copy["tool_calls"]:
#                 if isinstance(call, dict):
#                     serialized_tool_calls.append(call)
#                 else:
#                     serialized_tool_calls.append({
#                         "id": call.id,
#                         "function": {
#                             "name": call.function.name,
#                             "arguments": call.function.arguments
#                         },
#                         "type": call.type
#                     })

#             msg_copy["tool_calls"] = serialized_tool_calls

#         # Tool role is already serializable (tool_call_id is a string), no changes needed
#         serializable_history.append(msg_copy)

#     with open(path, "w") as f:
#         json.dump(serializable_history, f, indent=2)

def save_chat_history(user_id, chat_history):
    path = get_history_file_path(user_id)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Dump the chat history exactly as it is, assuming it's valid JSON-serializable
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)




def clean_openai_response(text):
    # Remove LaTeX-style display math (\[ ... \])
    text = re.sub(r'\\\[(.*?)\\\]', r'\1', text, flags=re.DOTALL)

    # Replace some common LaTeX expressions with plain equivalents
    text = text.replace(r'\frac', ' / ')
    text = text.replace(r'\text{', '')
    text = text.replace(r'}', '')
    text = text.replace(r'\\', '')

    # Replace Greek letters / symbols
    text = text.replace('Delta', 'Δ')

    # Remove remaining curly braces, dollar signs, and other escape characters
    text = re.sub(r'[{}$]', '', text)

    # Normalize multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

api = Blueprint('api', __name__)

@api.route('/hello')
def hello():
    return "API working fine"

@api.route('/chat/<user_id>', methods=['POST'])

def chat(user_id):
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Load chat history
    chat_history = load_chat_history(user_id)

    # Get OpenAI reply
    reply = get_openai_response(user_message, chat_history)

    # Save updated history
    save_chat_history(user_id, chat_history)
    

    if isinstance(reply, dict):
        return jsonify({**reply, "isuser": "false"})
    else:
        return jsonify({"reply": reply, "isuser": "false"})

