from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import uuid
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from ..extensions import mongo
from ..utils.database import MongoDBUserCollection


blueprint = Blueprint('api', __name__, url_prefix = '/api')
api = Api(blueprint, title='My API', version='1.0', description='A simple API')


ns = api.namespace('', description='User API')

signup_model = api.model('User_Signup', {
    'email': fields.String(required=True, description='The user email'),
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password'),
})

login_model = api.model('User_Login', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
})
signup_response_model = api.model('SignupResponse', {
    'email': fields.String(description='User email'),
    'username': fields.String(description='User username'),
    'error': fields.String(description='Error message'),
})


@ns.route('/signup')
class Signup(Resource):
    @ns.expect(signup_model, validate=True)
    #@ns.marshal_with(signup_response_model)
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
            return {"email": result["email"], "username": result["username"], "recipes": result['recipes'], "error": ""}, 200
        else:
            return {"email": "", "username": "", "error": "User failed to signup"}, 400

@ns.route('/login')
class Signup(Resource):
    @ns.expect(login_model, validate=True)
    #@ns.marshal_with(signup_response_model)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        result = current_app.mongodb_user.login_user(email, password)
        if result is not None:
            return (
                {"email": result["email"], "username": result["username"], "recipes": result["recipes"],  "error": ""}, 200
            )
        else:
            return (
                {"email": "", "username": "", "error": "User failed to login"},
                400
            )



@ns.route('/search_username')
class UserSearch(Resource):
    @ns.doc('search_username')
    @ns.expect(ns.parser().add_argument('username', type=str, required=False, help='Username query', location='args'))
    def get(self):
        args = request.args
        query = args.get("username", "")
        users= current_app.mongodb_user.search_usernames(query)
        user_list = [] 
        for user in users:
            user_data = {
                'email': user['email'],
                'username': user['username'],
                # Ensure recipes data is structured as a list of strings; adjust as necessary
                'recipes': user.get('recipes', [])
            }
            user_list.append(user_data)

        return {'users': user_list}
    

# api = Blueprint("api", __name__)

# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../../uploads")
# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)


# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# @api.route("/upload", methods=["POST"])
# def upload_file():
#     # Check if the post request has the file part
#     if "file" not in request.files:
#         return jsonify({"message": "No file part"}), 400
#     file = request.files["file"]
#     # If the user does not select a file, the browser submits an
#     # empty file without a filename.
#     if file.filename == "":
#         return jsonify({"message": "No selected file"}), 400
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(UPLOAD_FOLDER, filename))
#         return jsonify({"message": "File successfully uploaded"}), 200


# @api.route("/signup", methods=["POST"])
# def signup():

#     data = request.get_json()
#     email = data.get("email")
#     username = data.get("username")
#     password = data.get("password")
#     user_id = str(uuid.uuid4())

#     hashed_password = generate_password_hash(password)
#     result = current_app.mongodb_user.signup_user(email, username, password)

#     if result is not None:
#         return (
#             jsonify(
#                 {"email": result["email"], "username": result["username"], "error": ""}
#             ),
#             200,
#         )
#     else:
#         return (
#             jsonify({"email": "", "username": "", "error": "User failed to signup"}),
#             400,
#         )


# @api.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     result = current_app.mongodb_user.login_user(email, password)
#     if result is not None:
#         return (
#             jsonify(
#                 {"email": result["email"], "username": result["username"], "error": ""}
#             ),
#             200,
#         )
#     else:
#         return (
#             jsonify({"email": "", "username": "", "error": "User failed to login"}),
#             400,
#         )


# @api.route("/search_user", methods=["GET"])
# def search_user():
#     query = request.args.get("user", "")
#     username_list = current_app.mongodb_user.search_usernames(query)
#     result = {"usernames": username_list}
#     return jsonify(result), 200
