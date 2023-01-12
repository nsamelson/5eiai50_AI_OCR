import shutil
import os

def deleteFolder(folder_path) : 

    # Use the shutil.rmtree() function to delete the folder and all its contents
    shutil.rmtree(folder_path)

def createFolder(directory):
    # Download image from url
    # directory = "temp"
   if not os.path.exists(directory):
      os.makedirs(directory)

def empty(folder_path):
    deleteFolder(folder_path)
    createFolder(folder_path)