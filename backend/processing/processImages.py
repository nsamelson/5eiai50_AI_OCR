import numpy as np
import cv2

import tensorflow as tf
import os



def predict():
    # load the model
    model = tf.keras.models.load_model('models/digitsAndPrinted.model')
    output_labels = ['0','1','2','3','4','5','6','7','8','9',
        'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    ]
    
    # create var
    output = {}

    # while os.path.isdir(f"preprocessing/textbounding/outputchars/{wordNumber}"):
    for word in os.listdir(f"preprocessing/textbounding/outputchars/"):
        index = int(word) - 1
        
        outputWord = []
        for char in os.listdir(f"preprocessing/textbounding/outputchars/{word}"):
            img = cv2.imread(f"preprocessing/textbounding/outputchars/{word}/{char}")[:,:,0]
            img = np.invert(np.array([img]))

            prediction = model.predict(img, verbose=0)
            # print(f"This character is probably a {output_labels[np.argmax(prediction)]}")
            outputWord.append(output_labels[np.argmax(prediction)])
        
        output[index] = "".join(outputWord)
    return output

