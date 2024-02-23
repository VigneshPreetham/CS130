from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from ..extensions import mongo
import os
import uuid

api = Blueprint('api', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'message': 'File successfully uploaded'}), 200


@api.route('/signup', methods=['POST'])
def signup():
    db = mongo.cx['savor']
    users_collection = db['users']
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user_id = str(uuid.uuid4())
    


    hashed_password = generate_password_hash(password)

    result = users_collection.insert_one({"id:": user_id, "email": email, "password": hashed_password})

    return jsonify({"message": "User created successfully"}), 201


    