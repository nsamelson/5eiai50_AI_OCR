import numpy as np
import tensorflow as tf

from sklearn.model_selection import train_test_split

from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau

import os

# sources
# https://www.youtube.com/watch?v=bte8Er0QhDg
# https://keras.io/api/models/model_training_apis/
# https://www.kaggle.com/code/yassineghouzam/introduction-to-cnn-keras-0-997-top-6


# load training set
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# normalize the data
x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Split the train and the validation set for the fitting
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.1, random_state=2)

# create model
model = Sequential()

# CNN architechture : In -> [[Conv2D->relu]*2 -> MaxPool2D -> Dropout]*2 -> Flatten -> Dense -> Dropout -> Out
model.add(Conv2D(filters = 32, kernel_size = (5,5),padding = 'Same', activation ='relu', input_shape = (28,28,1)))
model.add(Conv2D(filters = 32, kernel_size = (5,5),padding = 'Same', activation ='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))


model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same', activation ='relu'))
model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'Same', activation ='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))


model.add(Flatten())
model.add(Dense(256, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(10, activation = "softmax"))

# Simple MLP model [784,256,128,10]
# model.add(Flatten(input_shape=(28,28)))
# model.add(Dense(256, activation = "relu"))
# model.add(Dense(128, activation = "relu"))
# model.add(Dense(10, activation = "softmax"))

# Compile the model
model.compile(optimizer="adam",loss="sparse_categorical_crossentropy", metrics=['accuracy'])

# Set a learning rate annealer
learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', 
                                            patience=3, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.00001)

# Parameters to train the model
epochs = 5 # iterations to go through the entire model
batch_size = 86 # number of samples per batch


model.fit(  x_train, y_train, 
            batch_size = batch_size, 
            epochs = epochs, 
            validation_data = (x_val, y_val), 
            steps_per_epoch = x_train.shape[0] // batch_size)

# save the model
model.save('backend/models/handDigits.model')

