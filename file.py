from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from matrixGen import updateMatrices
app = Flask(__name__)

path = os.getcwd()

UPLOAD_FOLDER = './dataset'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def temp():
   print(app.config['UPLOAD_FOLDER'])
   return render_template('index.html')
	
@app.route('/uploader', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      uploaded_file = request.files['file']
      if uploaded_file and allowed_file(uploaded_file.filename):
         dataset_file = open(UPLOAD_FOLDER+'/og.txt', 'a')
         for line in uploaded_file:
            dataset_file.write("\n")
            dataset_file.write(line.decode('utf-8').strip())
         updateMatrices(UPLOAD_FOLDER)
         return 'file uploaded successfully'
      else:
         return 'not a valid file type'
		
if __name__ == '__main__':
   app.run(debug = True)