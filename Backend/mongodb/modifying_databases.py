from pymongo import MongoClient 
import json

client = MongoClient("mongodb+srv://enak915:AMC11DgIsGELTyeC@trialdatabase.olxme32.mongodb.net/?retryWrites=true&w=majority&appName=TrialDatabase")
db = client['Backend']
chat_collection = db["chat_history"]
theme_collection = db["themes_history"]




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



