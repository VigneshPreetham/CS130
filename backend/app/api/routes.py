from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from ..extensions import mongo
import os

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
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Check if user already exists
    # user = mongo.db.users.find_one({"username": username})
    # if user:
    #     return jsonify({"error": "Username already exists"}), 409

    # Hash the password for security
    hashed_password = generate_password_hash(password)

    # Insert new user into the database
    print(mongo.db)
    mongo.db.users.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User created successfully"}), 201
