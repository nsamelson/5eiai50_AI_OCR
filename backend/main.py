from flask import *
from flask_cors import CORS
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials
from firebase_admin import db
import preprocessing.preprocessing as prep
import preprocessing.pdfToPng as ptp
import os
from PIL import Image
import utils.emptyFolder as empty
import processing.processImages as process

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

# PROCESS IMAGE TO TEXT
@app.route('/process/', methods=['POST'])
def processData():
       
   # Get url of picture
   items = request.get_json()
   imageName = items["img"]
   imageUrl = items["url"]
   folderName = items["folder"]
   
   # Create folder if not existing
   empty.createFolder("temp")
   
   # Download image from bucket
   blob = bucket.blob("processed/{}/{}".format(folderName,imageName))
   blob.download_to_filename("temp/"+imageName) 

   # Transform pdf into png
   if (imageName.endswith(".pdf")) :
      newImageName = ptp.transformIntoPng(imageName)
   else :
      newImageName = imageName
   
   # Preprocess
   prep.prepareCharacters("temp/"+newImageName)

   # Predict words
   output = process.predict()

   # Send the json to firebase/realtime database in a folder with its corresponding image
   output_ref = ref.child(folderName)
   output_ref.set({
      'Name': imageName,
      'url': imageUrl,
      'content':output
   })

   # Empty temp folder
   empty.empty("temp")
   
   # Send response
   response = jsonify({'success': 'The image has been processed!!!'})
   return response


if __name__ == '__main__':
   app.run()