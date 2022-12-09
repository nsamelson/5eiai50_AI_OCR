from flask import *
from flask_cors import CORS
# import json
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
    items = request.get_json()
    imageName = items["img"]
    imageUrl = items["url"]


    print(imageName, imageUrl)
    # TODO: call the preprocessing program
    # TODO: call the processing program (which will loop through every bouding box and send it to model)
    # TODO: call the post processing program which will send back a json
    # TODO: send the json to firebase/storage/processed in a folder with its corresponding image
    # TODO: send back a success response!
    
    response = jsonify({'success': 'The image has been processed!!!'})
    return response

# GET LIST OF UNPROCESSED IMAGES



if __name__ == '__main__':
   app.run()