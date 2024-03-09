from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from pymongo import MongoClient
import uuid
import os
from datetime import datetime
import boto3




class MongoDBUserCollection:
    def __init__(self, mongo):
        self.mongo = mongo
        self.db = self.mongo.cx['savor']
        self.users_collection = self.db['users']
    
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
        recipe_list = [] 

        self.users_collection.insert_one({"id": user_id, "email": email, "username": username, "password": hashed_password, "recipes": recipe_list, "created_on": formatted_now})
        user = self.users_collection.find_one({"email": email})

        return user

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

        return matches

class MongoDBRecipeCollection: 
    def __init__(self, mongo):
        self.mongo = mongo
        self.db = self.mongo.cx['savor']
        self.food_collection = self.db['food']
        self.users_collection = self.db['users']
    
    def insert_food(self, link_to_s3, creator):
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        recipe_id = str(uuid.uuid4())
        users = [] 
        self.food_collection.insert_one({"id": recipe_id, "link": link_to_s3, "created_by": creator, "users": user, "created_on": formatted_now })
        recipe = self.food_collection.find_one({"id": recipe_id})

        return recipe

   

class AmazonS3DB:
    def __init__(self):
        self.aws_access_key_id = None ####TODO
        self.aws_secret_access_key = None ###TODO
        self.s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)


    def upload_to_s3(self, file, filename):
        bucket_name = 'savor-recipe'
        filename_appended = f"{filename}-{int(time.time())}"

        s3.upload_fileobj(
            file,
            bucket_name,
            filename_appended,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

        file_url = f"https://{bucket_name}.s3.amazonaws.com/{filename}"
        return file_url

    


