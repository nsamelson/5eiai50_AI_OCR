import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
import tensorflow as tf
import os



# load the model
model = tf.keras.models.load_model('backend/models/handDigits.model')

imageNumber = 1

while os.path.isfile(f"backend/input/testDigits/{imageNumber}.png"):
    try:
        img = cv2.imread(f"backend/input/testDigits/{imageNumber}.png")[:,:,0]
        img = np.invert(np.array([img]))
        
        prediction = model.predict(img)
        print(f"This digit is probably a {np.argmax(prediction)}")

        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
    except:
        print("error")
    finally:
        imageNumber += 1 