from flask import Flask, flash, request, redirect, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import zipfile
from environs import Env

env = Env()
env.read_env()

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def upload_file(file, app):    

    file.save('/tmp/foo')
    size = os.path.getsize('/tmp/foo') / (1024 * 1024)
    
    if size >= 1:
        return 'The file is too big', 413
    

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    
    for folder, subfolders, filenames in os.walk('./uploads'):   
        if file.filename in filenames:
            return 'This file already exists', 409


    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # with open(f"./uploads/{file.filename}", "wb") as f:
        #     f.write(request.data)

        return f"{filename}", 201
    else:
        return 'Type file not allowed', 415
            


def show_all_files():   

    output = []
    
    for dirpath, dirnames, filenames in os.walk("./uploads"):
        if filenames == []:
            return 'Empty folder', 404
        output.append(filenames)

    return jsonify(output)



def show_filtered_files(type_file):   
    
    output = []
    
    for dirpath, dirnames, filenames in os.walk("./uploads"):
        if filenames == []:
            return 'The file does not exist', 404
        for name in filenames:
            if name.rsplit('.', 1)[1].lower() == type_file:
                output.append(name)
        

    return jsonify(output)



def download_file_url(file_name):
    try:
        return send_from_directory(directory="../uploads", path=f'{file_name}', as_attachment=True)
    except TypeError:
        return 'File not exist', 404
    


def compression(rate):
    if rate == 'ZIP_DEFLATED':
        return zipfile.ZIP_DEFLATED
    if rate == 'ZIP_BZIP2':
        return zipfile.ZIP_BZIP2
    if rate == 'ZIP_STORED':
        return zipfile.ZIP_STORED
    if rate == 'ZIP_LZMA':
        return zipfile.ZIP_LZMA



def download_zip():

    file_type = request.args.get("file_type")
    compression_rate = request.args.get("compression_rate")
    zip_type = compression(compression_rate)
    fantasy_zip = zipfile.ZipFile('./archive.zip', 'w')
    is_not_empty = False
    
    for folder, subfolders, files in os.walk('./uploads'):
    
        for file in files:
            if file.endswith(file_type):
                fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), './'), compress_type = zip_type)
                is_not_empty = True
    fantasy_zip.close()

    if is_not_empty:
        return send_from_directory(directory="../", path='archive.zip', as_attachment=True)
    else:
        return 'No files of this type were found', 404

   

