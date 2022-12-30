from flask import *
from flask_cors import CORS
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials

# Firebase setup
cred = credentials.Certificate('backend/config/firebase.json')
firebase_admin.initialize_app(cred, {
   'storageBucket': 'ocr-des-enfers.appspot.com'
})

bucket = storage.bucket()

# Flask setup
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# TEST SERVER ONLY
@app.route('/')
def hello_world():
   response = jsonify({'some': 'data'})
   return response

# PROCESS IMAGE INTO OCR
@app.route('/process/', methods=['POST'])
def processData():
       
   # Get url of picture
   items = request.get_json()
   imageName = items["img"]
   imageUrl = items["url"]

   print(imageName, imageUrl)

   # Download image from url
   blob = bucket.blob("unprocessed/"+imageName)
   blob.download_to_filename("backend/temp/"+imageName) 

   # TODO: call the preprocessing program 
   #    - detect text zone
   #    - (detect words)
   #    - detect characters and make bounding boxes in 28*28px
   # TODO: iterative call the processing program (which will loop through every bouding box and send it to model)
   # TODO: call the post processing program which will send back a json
   # TODO: send the json to firebase/storage/processed in a folder with its corresponding image
   # TODO: send back a success response!

   # TODO: remove temp content
   
   response = jsonify({'success': 'The image has been processed!!!'})
   return response

# GET LIST OF UNPROCESSED IMAGES



if __name__ == '__main__':
   app.run()