import os
import certifi
from pymongo import MongoClient
import json
from datetime import datetime


# Always store secrets like DB URI in environment variables
uri = os.environ.get("MONGO_URI")

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client['Backend']
chat_collection = db["chat_history"]
theme_collection = db["themes_history"]
theme_database = db["themes_database"]
checkpoint_collection = db["checkpoints_history"]




def make_data(chat_history, user_id: str, session_id: str):
    doc = {
        "user_id": user_id,
        "chat_session_id": session_id,
        "history": chat_history
    }
    chat_collection.insert_one(doc)
def insert_data(chat_data , user_id :str , session_id : str):
    
    chat_collection.update_one(
        {
            "user_id": user_id,
            "chat_session_id": session_id
        },
        {
            "$push": {"history": chat_data}
        }
    )

def retrieve_data(user_id: str, session_id: str):
    doc = chat_collection.find_one(
        {"user_id": user_id, "chat_session_id": session_id},
        {"_id": 0, "history": {"$slice": -10}}  # efficient slice
    )
    if doc and doc.get("history"):
        return doc["history"]   # ✅ Return Python list
    else:
        return []
    

def make_theme_data(theme_css, user_id: str, session_id: str):
    doc = {
        "user_id": user_id,
        "chat_session_id": session_id,
        "css": theme_css
    }
    theme_collection.insert_one(doc)

def insert_theme_data(theme_data , user_id :str , session_id : str):
    
    theme_collection.update_one(
        {"user_id": user_id, "chat_session_id": session_id},
        {"$set": {"css": theme_data}}  # Not $push
)

def retrieve_theme_data(user_id: str, session_id: str):
    doc = theme_collection.find_one(
        {"user_id": user_id, "chat_session_id": session_id},
        {"_id": 0, "css": 1}
    )
    if doc and isinstance(doc.get("css"), str):
        return doc["css"]  # ✅ Return CSS string directly
    else:
        return ""


# def get_css_from_theme_name(theme_name: str) -> str:
#     """
#     Reads `{theme_name}_css.json` from `themes_dir` and returns CSS string.
#     """
#     # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
#     # themes_dir = os.path.join(BASE_DIR, "html_css_cache")
#     # json_path = os.path.join(themes_dir, f"{theme_name}_css.json")
#     # print(json_path)
#     # if not os.path.exists(json_path):
#     #     raise FileNotFoundError(f"No CSS JSON file found for theme: {theme_name}")

#     # with open(json_path, 'r') as f:
#     #     data = json.load(f)

#     # css_content = data.get("css", "")
#     # if not css_content:
#     #     raise ValueError(f"No 'css' content found in {json_path}")

#     # return css_content


# def upload_theme_css(theme_name: str):
#     """
#     Reads the {theme_name}_css.json from disk and uploads it to MongoDB.
#     Fields: theme, css, created_at, updated_at.
#     If the theme already exists, it is updated.
#     """

#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
#     themes_dir = os.path.join(BASE_DIR, "html_css_cache")
#     json_path = os.path.join(themes_dir, f"{theme_name}_css.json")

#     if not os.path.exists(json_path):
#         raise FileNotFoundError(f"No CSS JSON file found for theme: {theme_name}")

#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     css_content = data.get("css", "")
#     if not css_content:
#         raise ValueError(f"No 'css' field found in {json_path}")

#     theme_database.update_one(
#         {"theme": theme_name},
#         {
#             "$set": {
#                 "css": css_content,
#                 "updated_at": datetime.now()
#             },
#             "$setOnInsert": {
#                 "theme": theme_name,
#                 "created_at": datetime.now()
#             }
#         },
#         upsert=True
#     )

#     print(f"Uploaded CSS for theme: {theme_name}")

def get_css_by_theme_name(theme_name: str) -> str:
    """
    Fetches the CSS string for a given theme_name from MongoDB's themes_database collection.

    Parameters:
        theme_name (str): The name of the theme to look up.

    Returns:
        str: The CSS string if found.

    Raises:
        ValueError: If the theme is not found or CSS is missing.
    """
    doc = theme_database.find_one({"theme_name": theme_name}, {"_id": 0, "css": 1})
    
    if not doc or "css" not in doc:
        raise ValueError(f"No CSS found for theme: {theme_name}")
    
    return doc["css"]

def get_json_by_theme_name(theme_name: str) -> str:

    doc = theme_database.find_one({"theme_name": theme_name}, {"_id": 0, "json": 1})
    
    if not doc or "json" not in doc:
        raise ValueError(f"No JSON found for theme: {theme_name}")
    
    return doc["json"]

def get_html_by_theme_name(theme_name: str) -> str:

    doc = theme_database.find_one({"theme_name": theme_name}, {"_id": 0, "html": 1})
    
    if not doc or "html" not in doc:
        raise ValueError(f"No JSON found for theme: {theme_name}")
    
    return doc["html"]




def store_css_and_json_for_user(user_id: str, css_content: str , json_content : str , json_id : str , html_content : str):
    """
    Stores a copy of the theme CSS under `themes_history` for the user.
    If a document already exists, updates it.
    """
    
    theme_collection.update_one(
        {"user_id": user_id , "json_id" : json_id},
        {   
            "$set": {
                "css": css_content,
                "json": json_content,
                "html" : html_content,
                "json_id" : json_id,
                "updated_at": datetime.now()
            },
            "$setOnInsert": {
                "created_at": datetime.now()
            }
        },
        upsert=True
    )
    print(f"Stored CSS and JSON for user_id={user_id}")


def retrieve_css_and_json_for_user(user_id: str) -> str:
    """
    Retrieves the stored CSS for a given user_id from `themes_history`.
    Returns the CSS string if found, otherwise raises an error.
    """
    record = theme_collection.find_one(
    {"user_id": user_id},
    sort=[("_id", -1)])  # sort by _id descending, latest document first 

    if not record or "css" not in record:
        raise ValueError(f"No stored CSS found for user_id: {user_id}")

    # css_content = record["css"]
    # json_content = record["json"]
    return record

def retrieve_json_for_user(json_id: str) -> str:
    """
    Retrieves the stored CSS for a given user_id from `themes_history`.
    Returns the CSS string if found, otherwise raises an error.
    """
    record = theme_collection.find_one({"json_id": json_id})

    if not record or "css" not in record:
        raise ValueError(f"No stored CSS found for user_id: {json_id}")

    # css_content = record["css"]
    # json_content = record["json"]
    return record

def save_checkpoint(user_id: str, checkpoint_id: str, data: dict) -> None:
    """
    Upserts a checkpoint document keyed by (user_id, checkpoint_id).

    Parameters
    ----------
    user_id : str
        The user’s unique identifier.
    checkpoint_id : str
        A logical name/slug for this checkpoint (e.g. "theme_selected").
    data : dict
        Arbitrary JSON‑serialisable data you want to persist.

    Behaviour
    ---------
    * If a document for (user_id, checkpoint_id) exists, it is **updated**.
    * Otherwise a new document is **inserted**.
    * Timestamps are maintained automatically.
    """
    checkpoint_collection.update_one(
        {"user_id": user_id, "checkpoint_id": checkpoint_id},
        {
            "$set": {
                "data": data,
                "updated_at": datetime.now()
            },
            "$setOnInsert": {
                "created_at": datetime.now()
            }
        },
        upsert=True
    )




def retrieve_checkpoint(user_id: str, checkpoint_id: str) -> dict:
    """
    Retrieves the checkpoint data for the given user and checkpoint ID.

    Parameters
    ----------
    user_id : str
        The user’s unique identifier.

    checkpoint_id : str
        The name or slug of the checkpoint to retrieve.

    Returns
    -------
    dict
        The stored data for the checkpoint.

    Raises
    ------
    ValueError
        If the checkpoint does not exist for the given user.
    """
    doc = checkpoint_collection.find_one(
        {"user_id": user_id, "checkpoint_id": checkpoint_id},
        {"_id": 0, "data": 1}
    )

    if not doc or "data" not in doc:
        raise ValueError(f"No checkpoint found for user_id: {user_id}, checkpoint_id: {checkpoint_id}")

    return doc["data"]





