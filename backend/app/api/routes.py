from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import uuid4
import boto3
from botocore.exceptions import ClientError

from ..extensions import mongo
from ..utils.database import MongoDBUserCollection

api = Blueprint('api', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/uploadrecipe', methods=['POST'])
def upload_recipe():
    data = request.get_json()
    # Check if the post request has the neccesary recipe data
    if 'name' not in data:
        return jsonify({'message': 'No name'}), 400
    if 'recipe' not in data:
        return jsonify({'message': 'No recipe'}), 400
    if 'creator_id' not in data:
        return jsonify({'message': 'No creator'}), 400
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    #upload file to s3
    if file and allowed_file(file.filename):
        try:
            filename = upload_photo_to_s3(file)
        except ClientError as e:
            return jsonify({'message': 'Error uploading photo to s3 - ' + e}), 400
    
    db = mongo.cx['savor']
    recipe_collection = db['recipes']
    name = data.get('name')
    recipe = data.get('recipe')
    creator_id = data.get('creator_id')
    photo_filename = filename
    recipe_id = str(uuid.uuid4())

    result = recipe_collection.insert_one({"id": recipe_id,
                                           "name": name,
                                           "recipe": recipe,
                                           "photo_filename": photo_filename,
                                           "creator_id": creator_id})
    
    return jsonify({"message": "Recipe successfully created"}), 201


def upload_photo_to_s3(file):
    s3 = boto3.client('s3')
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(file, S3_BUCKET, filename)

    except ClientError as e:
        print("Error uploading photo:", e)
        return e
    
    # after upload file to s3 bucket, return filename of the uploaded file
    return filename

@api.route('/addrecipe', methods=['POST'])
def add_recipe():
    data = request.get_json()
    # Check if the post request has the neccesary recipe data
    if 'user_id' not in data:
        return jsonify({'message': 'No user_id'}), 400
    if 'recipe_id' not in data:
        return jsonify({'message': 'No recipe_id'}), 400

    result = add_recipe_to_user(data.get("user_id"), data.get("recipe_id"))

    return jsonify({"message": "Recipe added to User successfully"}), 200

def add_recipe_to_user(user_id, recipe_id):
    db = mongo.cx['savor']
    user_collection = db['users']
    query = {"user_id": user_id}
    update = { "$push" : { "recipes" : recipe_id} }

    result = user_collection.update_one(query, update)
    
    return result


@api.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    user_id = str(uuid.uuid4())
    


    hashed_password = generate_password_hash(password)
    result = current_app.mongodb_user.signup_user(email, username, password)

    if result is not None:
        return jsonify({"message": "User created successfully"}), 201
    else:
        return jsonify({"message": "Email taken"}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    result = current_app.mongodb_user.login_user(email, password)
    if result is not None:
        email = result['email']
        return jsonify({"message": f"User logged in successfully with {email}"}), 201
    else:
        return jsonify({"message": "User failed to login"}), 201

@api.route('/search_user', methods=['GET'])
def search_user():
    query= request.args.get('user', '')
    username_list = current_app.mongodb_user.search_usernames(query)
    result = {"usernames": username_list}
    return jsonify(result), 201
    











    