from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from pymongo import MongoClient
import uuid
import os
from datetime import datetime




class MongoDBUserCollection:
    def __init__(self, mongo):
        self.mongo = mongo
        self.db = self.mongo.cx['savor']
        self.users_collection = self.db['users']
        self.food_collection = self.db['food']
    
    def email_exists(self, email):
        user = self.users_collection.find_one({"email": email})
        return bool(user)
    
    def signup_user(self, email, username, password):
        if self.email_exists(email):
            return None
        
        user_id = str(uuid.uuid4())
        hashed_password = generate_password_hash(password)
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        self.users_collection.insert_one({"id": user_id, "email": email, "username": username, "password": hashed_password, "created_on": formatted_now})
        return user_id
    
    def login_user(self, email, password):
        user = self.users_collection.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return user
        else:
            return None
    
    def search_usernames(self, username):
        exact_match = self.users_collection.find_one({"username": username}, {"_id": 0, "id": 1})
        regex_pattern = '^' + username
        partial_matches = self.users_collection.find({"username": {"$regex": regex_pattern, "$options": "i"}}, {"_id": 0, "id": 1})

        matches = list(partial_matches)

        if exact_match: 
            matches = [match for match in matches if match['id'] != exact_match['id']]
            matches.insert(0, exact_match)

        uuids = [match['id'] for match in matches]
        return uuids


    


