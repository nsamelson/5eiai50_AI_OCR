import numpy as np 
import pandas as pd 
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.layers.convolutional import Conv2D
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

# labels = ['0','1','2','3','4','5','6','7','8','9',
#     'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
#     'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# import data
dataset = pd.read_csv("characterRecognition/datasets/newDigitsAndPrinted.csv").astype('float32')
dataset.rename(columns={'0':'label'}, inplace=True)

# Splite data the X - Our data , and y - the prdict label
X = dataset.drop('label',axis = 1)
y = dataset['label']

# free some space
del dataset 

# split the data
x_train, x_test, y_train, y_test = train_test_split(X,y)

# Normalize the data
x_train = x_train / 255.0
x_test = x_test / 255.0

# Reshape image in 3 dimensions (height = 28px, width = 28px , canal = 1)
x_train = x_train.values.reshape(-1,28,28,1)
x_test = x_test.values.reshape(-1,28,28,1)

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

# Split the train and the validation set for the fitting
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size = 0.1, random_state=2)

# build the model
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


model.add(Dense(36, activation = "softmax"))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Parameters to train the model
epochs = 10 # iterations to go through the entire model
batch_size = 256 # number of samples per batch


# train the model
history = model.fit(x_train, y_train, 
        validation_data = (x_val, y_val), 
        epochs = epochs, 
        batch_size = batch_size,
        steps_per_epoch = x_train.shape[0] // batch_size)

# evaluate the model
scores = model.evaluate(x_test,y_test, verbose=0)
print("CNN Score:",scores[1])

# save the model
model.save('models/newDigitsAndPrinted.model')
