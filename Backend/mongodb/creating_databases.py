from pymongo import MongoClient 


client = MongoClient("mongodb+srv://enak915:AMC11DgIsGELTyeC@trialdatabase.olxme32.mongodb.net/?retryWrites=true&w=majority&appName=TrialDatabase")
db = client['Backend']
chat_collection = db["chat_history"]
chat_collection.create_index([("user_id", 1), ("chat_session_id", 1)])
themes_collection = db["themes_history"]
themes_collection.create_index([("user_id", 1)])

