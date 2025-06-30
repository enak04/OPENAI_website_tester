import os
import certifi
from pymongo import MongoClient


# Always store secrets like DB URI in environment variables
uri = "mongodb+srv://enak915:AMC11DgIsGELTyeC@trialdatabase.olxme32.mongodb.net/?retryWrites=true&w=majority&appName=TrialDatabase"

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client['Backend']

# Setup your collections
chat_collection = db["chat_history"]
chat_collection.create_index([("user_id", 1), ("chat_session_id", 1)])

themes_collection = db["themes_history"]
themes_collection.create_index([("user_id", 1)])

themes_collection = db["themes_database"]
themes_collection.create_index([("theme_name", 1)])


