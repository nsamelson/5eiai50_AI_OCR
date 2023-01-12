# 5eiai50_AI_OCR
AI project to transcribe written characters into text

## Introduction
This project is a webapp that is capable of producing machine-readable text from scanned documents in image (png, jpg, etc.) or pdf format.
It uses different techniques and technologies, such as machine learning, computer vision and web/mobile functionalities.

## Architecture
The project architecture is divided into 2 sections : frontend (which is a website app) and backend (containing the trained AIs).

Furthermore, all files and documents are stored in the cloud by using the services of Firebase : Firebase Storage and Firebase Realtime Database.
The storage service is used to store all the images and PDFs the user uploads. It is divided in 2 folders : 'unprocessed' and 'processed'. The Realtime Database is used to store the output of each processed file in a key-value pair format (JSON).

### Frontend
The frontend was developped in JavaScript, using Ionic, which is an open-source framework for building mobile applications with web technologies such as HTML, CSS, and JavaScript. While running, it can be accessed through the url http://localhost:8100/ .

The app is divided into 3 pages :
1. **Home page** : it is used to import images or PDFs from the user's phone or computer. The user is able to change the name of the file and then submit it.
The app checks if it's a PDF or an image file before sending it to the storage
2. **Imported files page** : this page contains all the unprocessed files the user submitted. From this page, the user is able to select an image to process or delete it.
3. **Processed files page** : this page shows a history of all the files that have been processed. When selecting a file, the user has a preview of the original image, as well as a text area with the detected text. The user is also able to manually modify the content of the text area and save it.


### Backend
The backend was developed in Python, using the Flask library. There is only one endpoint, which can be accessed through the url 127.0.0.1:5000/process, using a 'POST' method. The backend recieves a request from the frontend, containing three parameters: 
- imageName: the name of the image to be processed. This is useful for naming the temporary images when they are download to be processed.
- imageUrl: this is the url leading to the image location on Firebase. It is used to link it to the output text that will be detected
- folderName: the name of the of the folder the image is stored in, inside Firebase. Useful for naming the temporary folders on the backend system.

This is how the backend works to process a file:
1. The image to be processed is downloaded into a temporary location, on the backend machine storage.
2. The image goes through a pre-processing stage: 
- A pre-trained machine learning model is run on the image, using OpenCV's `dnn` package. This allows to identify the words present in the picture, and crops them into individual images
- Each 'word image' is then processed by OpenCV again, in order to extract individual characters and crop them to new individual pictures, but this time using traditional computer vision
- Each 'character image' is then resized to a suitable size for the character recognition software
3. Each 'character image' is run through the actual pre-trained character recognition model, which outputs the predicted text to a JSON file.
4. The JSON -encoded text is sent to Firebase Realtime Database.
5. The backend ultimately proceeds to cleaning up all temporary folders


## Features
#### Minimal
- [x] A web app, where I can upload image files or pdf files, process them, and get the results in a structured format and save them.
- [x] I want to browse the history of processed files.
- [x] I want to read digits anywhere on a page, or in a configurable zone of the page.
#### Intermediate
- [x] I want to be able to read printed characters anywhere on the page, or in a configurable zone of the page.
- [x] I can take pictures of pages directly from my smartphone.
#### Advanced
- [ ] I want to be able to read single letters or digits handwritten characters, anywhere on the page, or in a configurable zone of the page.
#### Awesome
- [ ] I want to be able to read complete sentences of handwriten characters, anywhere in the page, or in a configurable zone of the page.


## Usage
### Requirements
* Ionic
    - ```cd frontend```
    - ```npm install -g @ionic/cli``` to install ionic
    - ```npm install``` to install all depedencies
* Python
    - ```pip install -r requirements.txt``` to install all libraries
### Running the app
From a shell at the root of the project, run:
- Frontend server : 
    - ```cd frontend```
    - ```ionic serve``` or ```ionic serve --external``` to access the website from external devices on the same local network
- Backend server :
    - ```cd backend```
    - ```python3 main.py```


## Sources
- https://kenn7.github.io/AIproject/project/
- https://www.kaggle.com/code/zadiyounes/text-detection/notebook
- https://learn.microsoft.com/en-us/windows/ai/directml/gpu-tensorflow-wsl
- https://pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
- https://www.kaggle.com/code/yassineghouzam/introduction-to-cnn-keras-0-997-top-6
