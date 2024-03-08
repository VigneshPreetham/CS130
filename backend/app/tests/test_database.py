import unittest
from unittest.mock import patch
from app.utils.database import MongoDBUserCollection  
import mongomock


class TestMongoDBUserCollection(unittest.TestCase):
    @mongomock.patch(servers=(('server.example.com', 27017),))
    def setUp(self):
        self.mongo = mongomock.MongoClient('server.example.com')
        self.user_collection = MongoDBUserCollection(self.mongo)

        # Sample data
        self.sample_user = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
        }
        self.hashed_password = "hashed_password"  # Simplification for the test

    @patch('werkzeug.security.generate_password_hash')
    def test_signup_user(self, mock_generate_password_hash):
        mock_generate_password_hash.return_value = self.hashed_password

        result = self.user_collection.signup_user(self.sample_user["email"], self.sample_user["username"], self.sample_user["password"])
        
        self.assertIsNotNone(result)
        self.assertEqual(result["email"], self.sample_user["email"])
        self.assertEqual(result["username"], self.sample_user["username"])
        self.assertTrue(self.user_collection.email_exists(self.sample_user["email"]))

    def test_email_exists(self):
        # First, ensure no user exists
        self.assertFalse(self.user_collection.email_exists(self.sample_user["email"]))

        # After signup, check again
        self.user_collection.signup_user(self.sample_user["email"], self.sample_user["username"], self.sample_user["password"])
        self.assertTrue(self.user_collection.email_exists(self.sample_user["email"]))

    @patch('werkzeug.security.check_password_hash')
    def test_login_user(self, mock_check_password_hash):
        mock_check_password_hash.return_value = True

        self.user_collection.signup_user(self.sample_user["email"], self.sample_user["username"], self.sample_user["password"])
        result = self.user_collection.login_user(self.sample_user["email"], self.sample_user["password"])
        
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


if __name__ == '__main__':
    unittest.main()
