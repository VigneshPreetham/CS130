import unittest
from unittest.mock import patch
import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_dir)
from app.utils.database import MongoDBUserCollection, MongoDBRecipeCollection 
import mongomock
import uuid
from datetime import datetime


class TestMongoDBUserCollection(unittest.TestCase):
    @mongomock.patch(servers=(("server.example.com", 27017),))
    def setUp(self):
        self.mongo = mongomock.MongoClient("server.example.com")
        self.user_collection = MongoDBUserCollection(self.mongo)

        # Sample data
        self.sample_user = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
        }
        self.hashed_password = "hashed_password"  # Simplification for the test

    @patch("werkzeug.security.generate_password_hash")
    def test_signup_user(self, mock_generate_password_hash):
        mock_generate_password_hash.return_value = self.hashed_password

        result = self.user_collection.signup_user(
            self.sample_user["email"],
            self.sample_user["username"],
            self.sample_user["password"],
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["email"], self.sample_user["email"])
        self.assertEqual(result["username"], self.sample_user["username"])
        self.assertTrue(self.user_collection.email_exists(self.sample_user["email"]))

    def test_email_exists(self):
        # First, ensure no user exists
        self.assertFalse(self.user_collection.email_exists(self.sample_user["email"]))

        # After signup, check again
        self.user_collection.signup_user(
            self.sample_user["email"],
            self.sample_user["username"],
            self.sample_user["password"],
        )
        self.assertTrue(self.user_collection.email_exists(self.sample_user["email"]))

    @patch("werkzeug.security.check_password_hash")
    def test_login_user(self, mock_check_password_hash):
        mock_check_password_hash.return_value = True

        self.user_collection.signup_user(
            self.sample_user["email"],
            self.sample_user["username"],
            self.sample_user["password"],
        )
        result = self.user_collection.login_user(
            self.sample_user["email"], self.sample_user["password"]
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["email"], self.sample_user["email"])

    # def test_search_usernames(self):
    #     # Insert multiple users for testing search functionality
    #     usernames = ["testuser", "testuser1", "test", "anotheruser"]
    #     for username in usernames:
    #         self.user_collection.signup_user(f"{username}@example.com", username, "password123")

    #     exact_match_result = self.user_collection.search_usernames("testuser")
    #     partial_match_result = self.user_collection.search_usernames("test")
    #     print(partial_match_result)
    #     self.assertIn("testuser", [username for username in usernames if username in exact_match_result])
    #     self.assertTrue(any("test" in username for username in partial_match_result))


class TestMongoDBRecipeCollection(unittest.TestCase):
    @mongomock.patch(servers=(("server.example.com", 27017),))
    def setUp(self):
        self.mongo = mongomock.MongoClient("server.example.com")
        self.recipe_collection = MongoDBRecipeCollection(self.mongo)

        # Sample data for tests
        self.sample_recipe = {
            "link": "http://example.com/recipe.jpg",
            "name": "Chocolate Cake",
            "recipe": "Mix ingredients and bake.",
            "created_by": "John Doe",
            "file_name": "recipe.jpg",
        }

    def test_insert_recipe(self):
        result = self.recipe_collection.insert_recipe(**self.sample_recipe)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], self.sample_recipe["name"])

    def test_search_recipe(self):
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        # Insert a recipe to find later
        self.recipe_collection.food_collection.insert_one(
            {"id": str(uuid.uuid4()), "created_on": formatted_now, **self.sample_recipe}
        )
        results = self.recipe_collection.search_recipe(self.sample_recipe["name"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], self.sample_recipe["name"])

    def test_get_recipe_by_id(self):
        # Insert a recipe to retrieve by ID
        recipe_id = str(uuid.uuid4())
        self.recipe_collection.food_collection.insert_one(
            {"id": recipe_id, **self.sample_recipe}
        )
        result = self.recipe_collection.get_recipe_by_id(recipe_id)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], self.sample_recipe["name"])

    def test_get_recipes(self):
        # Setup - inserting a user with a recipe
        user_id = str(uuid.uuid4())
        recipe_id = str(uuid.uuid4())
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        self.recipe_collection.users_collection.insert_one(
            {"id": user_id, "recipes": [recipe_id]}
        )
        self.recipe_collection.food_collection.insert_one(
            {"id": recipe_id, "created_on": formatted_now, **self.sample_recipe}
        )

        recipes = self.recipe_collection.get_recipes(user_id)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]["name"], self.sample_recipe["name"])


if __name__ == "__main__":
    unittest.main()
