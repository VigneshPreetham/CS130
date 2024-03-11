from flask import Blueprint, request, jsonify, current_app, Response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import boto3
from botocore.exceptions import ClientError
import uuid
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import time
import base64
from io import BytesIO

from ..extensions import mongo, chatgpt
from ..utils.database import MongoDBUserCollection
from ..utils.database import AmazonS3DB


blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, title="My API", version="1.0", description="A simple API")
ns = api.namespace("", description="User API")


def upload_photo_to_s3(file, filename):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    S3_BUCKET = "cs130-app-photos"
    try:
        s3.upload_fileobj(file, S3_BUCKET, filename)

    except ClientError as e:
        print("Error uploading photo:", e)
        return e

    # after upload file to s3 bucket, return filename of the uploaded file
    file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
    return file_url


signup_model = api.model(
    "User_Signup",
    {
        "email": fields.String(required=True, description="The user email"),
        "username": fields.String(required=True, description="The user username"),
        "password": fields.String(required=True, description="The user password"),
    },
)

login_model = api.model(
    "User_Login",
    {
        "email": fields.String(required=True, description="The user email"),
        "password": fields.String(required=True, description="The user password"),
    },
)
signup_response_model = api.model(
    "SignupResponse",
    {
        "email": fields.String(description="User email"),
        "username": fields.String(description="User username"),
        "error": fields.String(description="Error message"),
    },
)


@ns.route("/search_recipe")
class RecipeSearch(Resource):
    # @ns.doc('search_recipe')
    @ns.expect(
        ns.parser().add_argument(
            "recipe",
            type=str,
            required=False,
            help="Recipe search query",
            location="args",
        )
    )
    def get(self):
        args = request.args
        query = args.get("recipe", "")
        recipes = current_app.mongodb_recipe.search_recipe(query)
        return {"recipes": recipes}


@ns.route("/user_info")
class UserInfo(Resource):
    @ns.expect(
        ns.parser().add_argument(
            "user_id",
            type=str,
            required=True,
            help="User ID to get information",
            location="args",
        )
    )
    def get(self):
        args = request.args
        user_id = args.get("user_id", "")
        user_recipes = current_app.mongodb_recipe.get_recipes(user_id)
        user = current_app.mongodb_user.get_username(user_id)
        return {"username": user["username"], "recipes": user_recipes}


add_recipe_parser = api.parser()
add_recipe_parser.add_argument(
    "user_id", type=str, required=True, help="User to add recipe to", location="args"
)
add_recipe_parser.add_argument(
    "recipe_id", type=str, required=True, help="Recipe to add", location="args"
)


@ns.route("/add_recipe")
class AddRecipe(Resource):
    @api.doc("add_recipe", parser=add_recipe_parser)
    def post(self):
        args = add_recipe_parser.parse_args()
        recipe_id = args["recipe_id"]
        user_id = args["user_id"]

        user_recipes = current_app.mongodb_recipe.get_recipes(user_id)
        for recipe in user_recipes:
            if recipe["id"] == recipe_id:
                return {"message": "User has already added recipe"}

        result = current_app.mongodb_user.add_recipe_to_user(user_id, recipe_id)
        user_recipes = current_app.mongodb_recipe.get_recipes(user_id)

        return {
            "message": "Recipe added to User successfully",
            "user_id": user_id,
            "recipes": user_recipes,
        }, 200
    
remove_recipe_parser = api.parser()
remove_recipe_parser.add_argument(
    'user_id', type=str, required=True, help='User to remove recipe from', location='args'
)
remove_recipe_parser.add_argument(
    'recipe_id', type=str, required=True, help='Recipe to remove', location='args'
)
@ns.route('/remove_recipe')
class RemoveRecipe(Resource):
    @api.doc('remove_recipe', parser=remove_recipe_parser)
    def post(self):
        args = remove_recipe_parser.parse_args()
        recipe_id = args['recipe_id']
        user_id = args['user_id']
        user_recipes = current_app.mongodb_recipe.get_recipes(user_id)
        if recipe_id not in [recipe['id'] for recipe in user_recipes]:
            return {"message": "User does not have this recipe"}

        result = current_app.mongodb_user.remove_recipe_from_user(user_id, recipe_id)
        user_recipes = current_app.mongodb_recipe.get_recipes(user_id)

        return {
            "message": "Recipe removed from User successfully", 
            "user_id": user_id, 
            "recipes": user_recipes
        }, 200   


@ns.route("/signup")
class Signup(Resource):
    @ns.expect(signup_model, validate=True)
    # @ns.marshal_with(signup_response_model)
    def post(self):
        # Your existing signup logic here
        data = request.get_json()
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        user_id = str(uuid.uuid4())

        hashed_password = generate_password_hash(password)
        result = current_app.mongodb_user.signup_user(email, username, password)
        if result is not None:
            return {
                "email": result["email"],
                "username": result["username"],
                "recipes": result["recipes"],
                "user_id": result["id"],
                "error": "",
            }, 200
        else:
            return {
                "email": "",
                "username": "",
                "error": "Email already exists, please try again with another email",
            }, 400


@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    # @ns.marshal_with(signup_response_model)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        result = current_app.mongodb_user.login_user(email, password)
        if result is not None:
            return (
                {
                    "email": result["email"],
                    "username": result["username"],
                    "recipes": result["recipes"],
                    "user_id": result["id"],
                    "error": "",
                },
                200,
            )
        else:
            return ({"email": "", "username": "", "error": "User failed to login"}, 400)


@ns.route("/search_username")
class UserSearch(Resource):
    @ns.doc("search_username")
    @ns.expect(
        ns.parser().add_argument(
            "username", type=str, required=False, help="Username query", location="args"
        )
    )
    def get(self):
        args = request.args
        query = args.get("username", "")
        users = current_app.mongodb_user.search_usernames(query)
        user_list = []
        for user in users:
            user_data = {
                "email": user["email"],
                "username": user["username"],
                # Ensure recipes data is structured as a list of strings; adjust as necessary
                "recipes": user.get("recipes", []),
                "user_id": user["id"],
            }
            user_list.append(user_data)

        return {"users": user_list}


@ns.route("/recipe_info")
class RecipeSearch(Resource):
    @ns.expect(
        ns.parser().add_argument(
            "recipe_id",
            type=str,
            required=True,
            help="Get recipe information by ID",
            location="args",
        )
    )
    def get(self):
        args = request.args
        recipe_id = args.get("recipe_id", "")
        recipe = current_app.mongodb_recipe.get_recipe_by_id(recipe_id)
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
        return recipe_data


from werkzeug.datastructures import FileStorage

upload_parser = api.parser()
upload_parser.add_argument(
    "file", location="files", type=FileStorage, required=True, help="Image file"
)
upload_parser.add_argument("user_id", type=str, required=True, help="User id")


@ns.route("/upload_image")
class ImageUpload(Resource):
    @api.doc("upload_image", parser=upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args["file"]  # This is a FileStorage instance
        user_id = args["user_id"]

        if uploaded_file:
            # For example, save the file
            filename = secure_filename(uploaded_file.filename)
            unique_filename = f"{filename}-{int(time.time())}"
            uploaded_file.seek(0)  # Ensure pointer is at start
            file_data = uploaded_file.read()

            # Create a new BytesIO object for uploading to S3
            bytes_io_for_upload = BytesIO(file_data)

            file_url = upload_photo_to_s3(bytes_io_for_upload, unique_filename)

            bytes_io_for_encoding = BytesIO(file_data)
            encoded_image = base64.b64encode(bytes_io_for_encoding.read()).decode(
                "utf-8"
            )

            food_name = chatgpt.image_identifier(encoded_image)
            generated_recipe = chatgpt.generate_recipe(food_name)
            recipe = current_app.mongodb_recipe.insert_recipe(
                file_url, food_name, generated_recipe, user_id, unique_filename
            )
            current_app.mongodb_user.add_recipe_to_user(user_id, recipe["id"])

            return {
                "message": "Image uploaded successfully, recipe generated",
                "id": recipe["id"],
                "filename": unique_filename,
                "s3_url": file_url,
                "name": food_name,
                "recipe": generated_recipe,
            }, 200
        else:
            return {"message": "No file uploaded"}, 400


@ns.route("/get_image")
class GetImage(Resource):
    @ns.expect(
        ns.parser().add_argument(
            "recipe_id",
            type=str,
            required=True,
            help="Get Image from S3 Using Recipe ID",
            location="args",
        )
    )
    def get(self):
        try:
            args = request.args
            recipe_id = args.get("recipe_id", "")
            recipe = current_app.mongodb_recipe.get_recipe_by_id(recipe_id)
            file_name = recipe["file_name"]
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
            S3_BUCKET = "cs130-app-photos"
            s3_response = s3.get_object(Bucket=S3_BUCKET, Key=file_name)
            image_bytes = s3_response["Body"].read()
            content_type = s3_response["ContentType"]
            return Response(image_bytes, mimetype=content_type)

        except Exception as e:
            return str(e), 404
