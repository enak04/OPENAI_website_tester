from flask import Blueprint, request, jsonify , Response
from .openai_client import get_openai_response
from database.modifying_databases import *
import re
import os
import json

HISTORY_DIR = "chat_histories"


def normalize_reply(reply):
    # Case 1: reply is a list (e.g., multiple tool call results) — pick the first valid one
    if isinstance(reply, list):
        for item in reply:
            if isinstance(item, dict):
                if isinstance(item.get("content"), list):
                    content_item = item["content"][0] if item["content"] else {}
                    return {**content_item, "isuser": "false"}
                else:
                    return {**item, "isuser": "false"}

    # Case 2: reply is a dict with content as a list
    elif isinstance(reply, dict) and isinstance(reply.get("content"), list):
        content_item = reply["content"][0] if reply["content"] else {}
        return {**content_item, "isuser": "false"}

    # Case 3: already flat
    elif isinstance(reply, dict):
        return {**reply, "isuser": "false"}

    # Fallback
    return {"content": str(reply), "isuser": "false"}




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
    session_id = "001"
    data = request.get_json()
    user_message = data.get("message", "")
    selected_theme = data.get("selected_theme")
    json_id = data.get("json_id")
    if selected_theme:
        # store_url = f"https://{selected_theme}.store.shoopy.in/"
        # store_id = user_id
        # result = call_fetch_html_css_api(store_url , store_id , base_url="http://127.0.0.1:5000")
        css_result = get_css_by_theme_name(selected_theme.lower())
        json_result = get_json_by_theme_name(selected_theme.lower())
        store_css_and_json_for_user(user_id , css_result , json_result , json_id)
        return {"timestamp" : datetime.now().isoformat(), "content" : "Here's your theme!" , "isuser" : "false"}

    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Load chat history
    chat_history = load_chat_history(user_id)

    # Get OpenAI reply
    reply = get_openai_response(user_message, chat_history , user_id , session_id , json_id)

    # Save updated history
    save_chat_history(user_id, chat_history)
    

    # if isinstance(reply, dict):
    #     return jsonify({**reply, "isuser": "false"})
    # else:
    #     return jsonify({"reply": reply, "isuser": "false"})
    
    return jsonify(normalize_reply(reply))

@api.route('/checkpoint/<user_id>/<checkpoint_id>', methods=['POST'])
def checkpoint_handler(user_id, checkpoint_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Save the checkpoint
    save_checkpoint(user_id, checkpoint_id, data)
  

    return Response(status=204)


@api.route('/checkpoint/<user_id>/<checkpoint_id>/<json_id>', methods=['GET'])
def get_checkpoint(user_id, checkpoint_id , json_id):
    try:
        data = retrieve_checkpoint(user_id, checkpoint_id)
        return jsonify({
            "user_id": user_id,
            "checkpoint_id": checkpoint_id,
            "data": data
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    

@api.route('/', methods=['GET'])
def retrieve_json():
    json_id = request.args.get('id')
    if json_id:
        result = retrieve_json_for_user(json_id)
        result2 = json.loads(result["json"])
        return jsonify ({"json" : result2["payload"]})
    else:
        return jsonify({"error": "No ID provided"}), 400





