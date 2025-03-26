# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 08:37:04 2023

@author: ethan
"""

#%% LAB 13
# ETHAN D ROBINSON
# PHSCS 430, FALL 2023
#%% P13.1
# explain the readings to the TA
#%% P13.2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 04:55:41 2020

@author: parke
"""

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
import tensorflow as tf

data = np.array([[1.4, 20.], [1.8, 30.], [2.1, 37.], [2.2, 45.], 
                 [2.3,26.], [2.9, 86.], [3.5, 67.], [3.6, 100.], 
                 [4.2, 72.], [4.6, 82.], [4.7, 99.]])

[X_train,Y_train] = data.transpose()

model = Sequential()
model.add(Dense(1, activation='linear', input_dim=1))
sgd = tf.keras.optimizers.SGD(lr=0.03) #lr is the learning rate
model.compile(loss='mean_squared_error',optimizer=sgd)

#this command does the minimization
model.fit(X_train, Y_train, epochs=100, verbose=1)

#displays some useful info, note how there are only 2 fitting parameters
model.summary()

# the predict function on the next line assumes an
# array of inputs so we need to put 2.7 inside an array
x = np.array([2.7])

#... and predicted_y is likewise an array of predicted outputs
predicted_y = model.predict(x)
print('For x={:f} the predicted y is: {:f}'.format(float(x),float(predicted_y)))

#%% P13.3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 04:55:43 2020

@author: parke
"""

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
from keras.datasets import boston_housing
import tensorflow as tf

(X_train, Y_train), (X_validate, Y_validate) = boston_housing.load_data()

#description here: https://github.com/eric-bunch/boston_housing

print(X_train.shape)
print(Y_train.shape)
print(X_validate.shape)
print(Y_validate.shape)

model = Sequential()
model.add(Dense(30, activation='relu',input_dim=13))
model.add(Dense(20, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(1, activation='linear'))
optimizer_choice = tf.keras.optimizers.Adam(lr=0.1)
model.compile(loss='mean_squared_logarithmic_error', optimizer=optimizer_choice, metrics=['mse'])
model.fit(X_train, Y_train, batch_size=64, epochs=200, verbose=1) #what is batch size?
model.summary()
score = model.evaluate(X_validate, Y_validate, verbose=0)

print('The loss value and accuracy of the test set is: ' + str(score))

#prediction for a specific input
test_num = 27 #randomly chosen number
x = np.array([X_validate[test_num]])
predicted_y = model.predict(x)
print('For input parameters x = ')
print(X_validate[test_num])
print('the predicted y (median value of home, in $1000s) is: {:f} '.format(float(predicted_y)))
print('and the actual y value was: {:f}'.format(float(Y_validate[test_num])))

#%% P13.4

# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 04:55:45 2020

@author: parke
"""

import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import keras.utils as utils
from keras.datasets import mnist

(X_train, Y_train), (X_validate, Y_validate) = mnist.load_data()
#X_train has dimensions (60000, 28, 28): 60,000 images which are 28x28

#number of data points in training set traditionally called m
m = X_train.shape[0]

#view two of the images, images 10 and 11 just chosen randomly
plt.figure(1)
plt.imshow(X_train[10])
plt.figure(2)
plt.imshow(X_train[11])

#view the image labels corresponding to the two images
print('image 10 label:' + str(Y_train[10]))
print('image 11 label:' + str(Y_train[11]))

#There are three problems with the supplied data.

# First, the convolutional layers will expect the image data
# to be in a "channel", even if it's just a monochrome channel.
# Let's fix that.
X_train = X_train.reshape(m, 28, 28, 1)

#Now the dims are (60000, 28, 28, 1)

# Side note: this would need to be (60000, 28, 28, 3)
# if we had RGB image data

# Secondly, neural nets tend to work best for inputs
# between 0 and 1, so let's normalize the data
X_train = X_train/255

# Thirdly, the y-values are just digits rather than the
# needed arrays of size 10 (corresponding to probabilities
# of digits 0-9, respectively). There's a built-in function
# called "to_categorical" for that.
Y_train = utils.to_categorical(Y_train, 10) #now has dims (60000, 10)

#view the new image labels corresponding to the two images
print('new image 10 label:' + str(Y_train[10]))
print('new image 11 label:' + str(Y_train[11]))

#Now to define the neural net structure and hyperparameters.

model = Sequential()

#layer 1:
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28,28,1)))

#layer 2:
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

#layer 3:
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))

#layer 4 (output):
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam',
metrics=['accuracy'])

# And now we train the model. This takes a long time, perhaps
# 10 mins depending on your computer, since there are over
# 600,000 adjustable parameters in the 4-layer model we have
# just defined! The bulk of them come from the 4608 outputs
# from layer 2 connecting densely to 128 nodes in layer 3.
# The "batch_size" setting in the command indicates how many
# training inputs it should consider at once as it is adjusting
# the parameters, and the "epochs" number indicates how many
# complete iterations through the entire training set it should do.

model.fit(X_train, Y_train, batch_size=32, epochs=6, verbose=1)
model.summary()

# And now it's done! We can make predictions. To get a general sense as to
# the quality of the NN predictions, we can use the validation set... but we
#must first address the same three issues we did with the training set.

m_test = X_validate.shape[0]

print('Test set has {:d} entries.'.format(m_test))

X_validate = X_validate.reshape(m_test, 28, 28, 1)
X_validate = X_validate/255 # to normalize X values between 0 and 1
Y_validate = utils.to_categorical(Y_validate, 10)

#the output of this next command will tell you how good the NN did on the test set
score = model.evaluate(X_validate, Y_validate, verbose=0)
print('The loss value and accuracy of the test set is: ' + str(score))


#It's also fun to look at predictions for single examples. "140" here was just
#a random selection. You can copy and paste these next few lines into the
#console with different test numbers to see an image along with its predicted
#output value.

testimagenumber = 140
singletest=X_validate[testimagenumber]

plt.figure(3)

#must convert back to format imshow can use
plt.imshow(np.round(singletest*255).squeeze())

#model.predict expects an array, so give it an array of length 1
singleprediction = model.predict(np.array([singletest]))[0]

#argmax function converts from the length 10 output array back to a single digit
singleprediction = np.argmax(singleprediction)

print('The prediction for image {:d} is: {:d} '.format(testimagenumber, singleprediction))

#%% 13.5
# First, some boilerplate
# Name: Dumb Ultron
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import keras.utils as utils
from keras.datasets import mnist

# And get the data sets
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Then load them up
iris = load_iris()
X = iris['data'] #150 entries, 4 parameters each
Y = iris['target'] #150 entries, values of 0, 1, or 2
names = iris['target_names']
feature_names = iris['feature_names']

X_train, X_validate, Y_train, Y_validate \
        = train_test_split(X, Y, test_size=0.333)
        
# Reformat the Y_train dataset
Y_train = utils.to_categorical(Y_train, 3) # Now has dimensions of 100x3 instead of just a vector

# We want a sequential model
model = Sequential()

# And we build our model
#layer 1:
model.add(Dense(4, activation='relu',input_dim=4))

# Layer 3:
model.add(Dense(64, activation='relu'))

#layer 2:
model.add(Dense(16, activation='relu'))

model.add(Dense(4, activation='relu'))

model.add(Dense(4, activation='relu'))

model.add(Dense(4, activation='relu'))

model.add(Dense(3, activation='relu'))

#layer 4:
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam',
metrics=['accuracy'])

# Train the Model
model.fit(X_train, Y_train, batch_size=42, epochs=6, verbose=1)
model.summary()

#reformat Y_validate
Y_validate = utils.to_categorical(Y_validate, 3)

#the output of this next command will tell you how good the NN did on the test set
score = model.evaluate(X_validate, Y_validate, verbose=0)
print('The loss value and accuracy of the test set is: ' + str(score))
