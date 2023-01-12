from flask import *
from flask_cors import CORS
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials
from firebase_admin import db
import preprocessing.preprocessing as prep
import os


# Firebase setup
cred = credentials.Certificate('./config/firebase.json')
firebase_admin.initialize_app(cred, {
   'storageBucket': 'ocr-des-enfers.appspot.com',
   "databaseURL": "https://ocr-des-enfers-default-rtdb.europe-west1.firebasedatabase.app/" 
})

bucket = storage.bucket()
ref = db.reference('processed')


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
   print("Got following content : ")
   print(items)
   imageName = items["img"]
   imageUrl = items["url"]
   folderName = items["folder"]

   # Download image from url
   directory = "temp"
   if not os.path.exists(directory):
      os.makedirs(directory)
   
   blob = bucket.blob("processed/{}/{}".format(folderName,imageName))
   blob.download_to_filename("temp/"+imageName) 

   # TODO: call the preprocessing program 
   prep.prepareCharacters("./backend/temp/"+imageName)

   #    - make bounding boxes in 28*28px
   # TODO: iterative call the processing program (which will loop through every bouding box and send it to model)
   # TODO: call the post processing program which will send back a json

   # Send the json to firebase/realtime database in a folder with its corresponding image
   output_ref = ref.child(folderName)
   output_ref.set({
      'Name': imageName,
      'url': imageUrl,
      'content':{
         "test" :"1, 2",
         "other test": "1,2,3,4"
      }
   })
   # TODO: send back a success response!

   # TODO: remove temp content
   
   response = jsonify({'success': 'The image has been processed!!!'})
   return response


if __name__ == '__main__':
   app.run()