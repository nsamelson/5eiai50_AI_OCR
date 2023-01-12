import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
import tensorflow as tf
import os



# load the model
model = tf.keras.models.load_model('models/newDigitsAndPrinted.model')
output_labels = ['0','1','2','3','4','5','6','7','8','9',
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    ]
    # 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
imageNumber = 1



while os.path.isfile(f"characterRecognition/input/testAllTogether/{imageNumber}.png"):
    try:
        img = cv2.imread(f"characterRecognition/input/testAllTogether/{imageNumber}.png")[:,:,0]
        img = np.invert(np.array([img]))
        
        prediction = model.predict(img)
        # print(f"This character is probably a {np.argmax(prediction)}")
        print(f"This character is probably a {output_labels[np.argmax(prediction)]}")

        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
    except:
        print("error")
    finally:
        imageNumber += 1 