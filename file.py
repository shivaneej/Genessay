from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from matrixGen import updateMatrices
from flask import Flask, request, redirect
from flask_cors import CORS
from flask import *
import time
app = Flask(__name__)
cors = CORS(app)

path = os.getcwd()

UPLOAD_FOLDER = './dataset'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt'])
DATASET_FILE_NAME = '/og.txt'


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def login():
   return render_template('login.html')


@app.route('/admin')
def admin_page():
   print(app.config['UPLOAD_FOLDER'])
   return render_template('file.html')

@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':  
      uploaded_file = request.files['inpFile']
      if uploaded_file and allowed_file(uploaded_file.filename):
         dataset_file = open(UPLOAD_FOLDER + DATASET_FILE_NAME, 'r')
         file_contents = uploaded_file.read().decode("utf-8")
         file_contents = file_contents.replace('\r', ' ')
         new_samples = [content.strip() for content in file_contents.split('\n \n') if content]
         old_samples = [content for content in dataset_file.read().split('\n\n') if content]
         print(new_samples)
         total_samples = new_samples + old_samples
         total_samples = [content.strip() for content in total_samples if content]
         unique_samples = set(total_samples)
         unique_samples_list = list(unique_samples)
         with open(UPLOAD_FOLDER + DATASET_FILE_NAME, 'w') as overwritten_file:
            for sample in unique_samples_list:
               overwritten_file.write("%s\n\n" % sample)
         print("File Uploaded successfully")
         return 'file uploaded successfully', 200
      else:
         return 'not a valid file type', 422

@app.route('/update')
def update():
   # updateMatrices(UPLOAD_FOLDER)
   for i in range(100):
      print(i)
      time.sleep(0.5)
   return "", 200
   

   


if __name__ == '__main__':
   app.run(debug = True)



      