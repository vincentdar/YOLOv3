# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2021-12-09 09:57:49
# @Last Modified by:   Your name
# @Last Modified time: 2021-12-15 16:25:43
from flask import Flask, jsonify, flash, request, url_for, redirect, session, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from ImageDetector import ImageDetector

UPLOAD_FOLDER = 'Uploads'
RESULT_FOLDER = 'result'
ALLOWED_EXTENSION = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['SECRET_KEY'] = 'thisisasecret'

imageDetector = ImageDetector()

def allowed_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(type(file))
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            my_uuid = str(uuid.uuid4())
            filename = my_uuid + ".jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status = imageDetector.predict(filename)
            print("UUID:", my_uuid)
            print("Status:", status)
            print("DETECTOR WORKING")
            return redirect(url_for('download_file', name=filename))
    return render_template('index.html')


@app.route('/results/<name>')
def download_file(name):
    return send_from_directory(app.config["RESULT_FOLDER"], name)
    
    
if __name__ == '__main__':   
    app.run(host='0.0.0.0',debug=True)
    
    