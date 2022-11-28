import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import Sequential

from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras import backend as K
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.callbacks import ReduceLROnPlateau


# source
# https://www.kaggle.com/code/yairhadad1/cnn-for-handwritten-alphabets

# import data
dataset = pd.read_csv("backend/training/A_Z Handwritten Data.csv").astype('float32')
dataset.rename(columns={'0':'label'}, inplace=True)

# Splite data the X - Our data , and y - the prdict label
X = dataset.drop('label',axis = 1)
y = dataset['label']

# split the data
x_train, X_test, y_train, y_test = train_test_split(X,y)

# scale data
standard_scaler = MinMaxScaler()
standard_scaler.fit(x_train)

x_train = standard_scaler.transform(x_train)
X_test = standard_scaler.transform(X_test)

# reshape into 28x28 pixels
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

# # Split the train and the validation set for the fitting
# x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.1, random_state=2)

# build the model
model = Sequential()

# model.add(Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(0.3))
# model.add(Flatten())
# model.add(Dense(128, activation='relu'))
# model.add(Dense(len(y.unique()), activation='softmax'))

# CNN architechture : input -> conv -> maxpool -> conv -> maxpool ......
#   -> flattened vector-> hidden layer -> hidden layer -> softmax layer
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(28,28,1)))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))

model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding = 'same'))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))

model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding = 'valid'))
model.add(MaxPool2D(pool_size=(2, 2), strides=2))

model.add(Flatten())

model.add(Dense(64,activation ="relu"))
model.add(Dense(128,activation ="relu"))
model.add(Dense(26,activation ="softmax"))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Parameters to train the model
epochs = 30 # iterations to go through the entire model
batch_size = 200 # number of samples per batch


# train the model
history = model.fit(x_train, y_train, 
        validation_data = (X_test, y_test), 
        epochs = epochs, 
        batch_size = batch_size,
        steps_per_epoch = x_train.shape[0] // batch_size)

# evaluate the model
scores = model.evaluate(X_test,y_test, verbose=0)
print("CNN Score:",scores[1])

# save the model
model.save('backend/models/handCharacters.model')