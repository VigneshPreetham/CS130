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
        exact_match = self.users_collection.find_one({"username": username})
        
        regex_pattern = '^' + username
        partial_matches = self.users_collection.find({"username": {"$regex": regex_pattern, "$options": "i"}})
        matches = list(partial_matches)
        if exact_match: 
            matches = [match for match in matches if match['id'] != exact_match['id']]
            matches.insert(0, exact_match)
           
        return matches

    def add_recipe_to_user(self, user_id, recipe_id):
        query = {"user_id": user_id}
        update = { "$push" : { "recipes" : recipe_id} }

        result = self.users_collection.update_one(query, update)
    
        return result
    
    def get_username(self, user_id):
        return self.users_collection.find_one({"user_id": user_id})



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
    
    def get_recipes(self, user_id):
        recipe_ids = self.users_collection.find_one({"user_id": user_id}).recipes

        recipes = []
        for recipe_id in recipe_ids:
            
            recipe = self.food_collection.find_one({"recipe_id": recipe_id})
            recipes.append(recipe)
        
        return recipes
    
    def search_recipe(self, recipe_search):
        exact_match = self.recipe_collection.find_one({"name": recipe_search})

        regex_pattern = recipe_search
        partial_matches = self.recipe_collection.find({"name": {"$regex": regex_pattern, "$options": "i"}}).limit(20)
        matches = list(partial_matches)
        if exact_match:
            matches.remove(exact_match)
            matches.insert(0, exact_match)
        
        return matches

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

    


