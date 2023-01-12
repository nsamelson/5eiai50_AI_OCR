# 5eiai50_AI_OCR
AI project to transcript written characters into text

## Introduction


## Architecture
The project architecture is divided into 2 sections : frontend (which is a website app) and backend (containing the trained AI). 

Furthermore, all files and documents are stored in the cloud by using the services of Firebase : Storage and Realtime Database.
The storage service is used to store all the images and PDFs the user sent. It is divided into 2 folders : unprocessed and processed. Realtime Database is used to store the output of each processed file in a key-value pair format (JSON).

### Frontend
The frontend was developped in Ionic, which is an open-source framework for building mobile applications with web technologies such as HTML, CSS, and JavaScript. 

The app is divided into 3 pages :
1. **Home page** : it is used to import images or PDFs from the user's phone or computer. The user is able to change the name of the file and then submit it.
The app checks if it's a PDF or an image file before sending it to the storage
2. **Imported files page** : this page contains all the unprocessed files the user submitted. From this page, the user is able to select an image to process or delete it.
3. **Processed files page** : this page shows all the files that are processed. When selecting a file, the user has a preview of the original image, as well as a text area with the detected text. The user is also able to modify the content of the text area and save it.



### Backend

## App capabilities



## Requirements
* Ionic
    - ```cd frontend```
    - ```npm install -g @ionic/cli``` to install ionic
    - ```npm install``` to install all depedencies
* Python
    - ```pip install -r requirements.txt``` to install all libraries


## Run the app
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
