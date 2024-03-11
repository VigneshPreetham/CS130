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
        query = {"id": user_id}
        update = { "$push" : { "recipes" : recipe_id} }

        result = self.users_collection.update_one(query, update)
    
        return result
    
    def add_recipe_to_user(self, user_id, recipe_id):
        user_query = {"id": user_id}
        user_update = { "$push" : { "recipes" : recipe_id} }

        result = self.users_collection.update_one(user_query, user_update)

        recipe_query = {"id": recipe_id}
        recipe_update = { "$push" : { "users_added" : user_id} }

        self.food_collection.update_one(recipe_query, recipe_update)

        return result

    def remove_recipe_from_user(self, user_id, recipe_id):
        user_query = {"id": user_id}
        user_update = { "$pull" : { "recipes" : recipe_id} }

        result = self.users_collection.update_one(user_query, user_update)

        recipe_query = {"id": recipe_id}
        recipe_update = { "$pull" : { "users_added" : user_id} }

        self.food_collection.update_one(recipe_query, recipe_update)

        return result
    
    def get_username(self, user_id):
        return self.users_collection.find_one({"id": user_id})



class MongoDBRecipeCollection: 
    def __init__(self, mongo):
        self.mongo = mongo
        self.db = self.mongo.cx['savor']
        self.food_collection = self.db['food']
        self.users_collection = self.db['users']
    
    def insert_recipe(self, link, name, recipe, created_by, file_name):
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        recipe_id = str(uuid.uuid4())
        users_added = []
        self.food_collection.insert_one({"id": recipe_id, "link": link, "file_name": file_name, "name": name,  "recipe": recipe, "created_by": created_by,  "created_on": formatted_now, "users_added": users_added})
        recipe = self.food_collection.find_one({"id": recipe_id})

        return recipe
    
    def get_recipes(self, user_id):
        user = self.users_collection.find_one({"id": user_id})

        if(user):
            recipe_ids = user["recipes"]
        else:
            return []

        recipes = []
        for recipe_id in recipe_ids:
            
            recipe = self.food_collection.find_one({"id": recipe_id})
            recipe_data = {
                'id': recipe['id'] if 'id' in recipe.keys() else "",
                'name': recipe['name'] if 'name' in recipe.keys() else "",
                'recipe': recipe['recipe'] if 'recipe' in recipe.keys() else "",
                'created_by': recipe["created_by"] if 'created_by' in recipe.keys() else "",
                'created_on': recipe["created_on"] if 'created_on' in recipe.keys() else "", 
                'link': recipe['link'] if 'link' in recipe.keys() else "",
                'users_added': recipe['users_added'] if 'users_added' in recipe.keys() else [],
                'file_name': recipe['file_name'] if 'file_name' in recipe.keys() else ""
            }
            recipes.append(recipe_data)
        
        return recipes
    
    def search_recipe(self, recipe_search):
        exact_match = self.food_collection.find_one({"name": recipe_search})

        regex_pattern = recipe_search
        partial_matches = self.food_collection.find({"name": {"$regex": regex_pattern, "$options": "i"}}).limit(20)
        matches = list(partial_matches)
        if exact_match:
            matches.remove(exact_match)
            matches.insert(0, exact_match)
        
        recipes = []
        for match in matches:
            recipe_data = {
                'id': match['id'] if 'id' in match.keys() else "",
                'name': match['name'] if 'name' in match.keys() else "",
                'recipe': match['recipe'] if 'recipe' in match.keys() else "",
                'created_by': match["created_by"] if 'created_by' in match.keys() else "",
                'created_on': match["created_on"] if 'created_on' in match.keys() else "", 
                'link': match['link'] if 'link' in match.keys() else "",
                'users_added': match['users_added'] if 'users_added' in match.keys() else [],
                'file_name': match['file_name'] if 'file_name' in match.keys() else ""
            }
            recipes.append(recipe_data)

        return recipes


    def get_recipe_by_id(self, recipe_id):            
        recipe = self.food_collection.find_one({"id": recipe_id})

        if recipe is not None:
            return recipe
        else:
            return None



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

    


