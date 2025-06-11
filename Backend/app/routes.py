from flask import Blueprint, request, jsonify
from .openai_client import get_openai_response
import re
import os
import json

HISTORY_DIR = "chat_histories"

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

def get_history_file_path(user_id):
    return os.path.join(HISTORY_DIR, f"{user_id}.json")

def load_chat_history(user_id):
    path = get_history_file_path(user_id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_chat_history(user_id, chat_history):
    path = get_history_file_path(user_id)

    # Convert all messages to serializable format
    serializable_history = []
    for msg in chat_history:
        msg_copy = msg.copy()

        # Convert tool_calls (which are objects) to dicts
        if "tool_calls" in msg_copy and isinstance(msg_copy["tool_calls"], list):
            tool_calls_serialized = []
            for tool_call in msg_copy["tool_calls"]:
                tool_calls_serialized.append({
                    "id": tool_call.id,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    },
                    "type": tool_call.type
                })
            msg_copy["tool_calls"] = tool_calls_serialized

        serializable_history.append(msg_copy)

    with open(path, "w") as f:
        json.dump(serializable_history, f, indent=2)



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

@api.route('/chat', methods=['POST'])

def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    user_id = "default"  # Pass unique user ID from frontend if possible

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Load chat history
    chat_history = load_chat_history(user_id)

    # Get OpenAI reply
    reply = get_openai_response(user_message, chat_history)

    # Save updated history
    save_chat_history(user_id, chat_history)

    return jsonify({"reply": reply})
