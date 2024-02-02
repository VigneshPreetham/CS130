from flask import current_app, flash, redirect, request, url_for, Blueprint
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return 'Hello, World!'

#from . import main

# @main.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
#         return 'File successfully uploaded'
#     else:
#         return 'Allowed file types are png, jpg, jpeg, gif'

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}