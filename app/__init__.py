
from flask import Flask, flash, request, redirect, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from environs import Env
import os
import zipfile
from kenzie import image

env = Env()
env.read_env()

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'bcimages'

image.create_upload_folder()


@app.route("/upload", methods=["POST"])
def upload():    
    
    if 'file' not in request.files:
            flash('No file part')
            return 'No file part'
    
    file = request.files["file"]
    return image.upload_file(file, app)
            

        
@app.route("/files", methods=["GET"])
def get_all_files():   

    return image.show_all_files()



@app.route("/files/<string:type_file>", methods=["GET"])
def get_filtered_files(type_file):   
    
    return image.show_filtered_files(type_file)



@app.route("/download/<string:file_name>")
def download_file(file_name):
    return image.download_file_url(file_name)
    


@app.route("/download-zip")
def get_download_zip():

   return image.download_zip()

   

