# first neural network with keras - predictions

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import os
import numpy as np
import time

#varNames = ['inning', 'vis score', 'home score', 'erahome', 'eraAway', 'bbhome', 'bbaway', 'hrhome','hraway', 'elo1pre', 'elo2pre', 'rating1_pre', 'rating2_pre' , ' GB_home', 'RS_home', 'RA_home', 'wins_home', 'losses_home', 'winper_home', ' GB_Away', 'RS_away', 'RA_away', 'wins_away', 'losses_away', 'winper_away']


##SPECIFY MODEL PARAMETERS HERE##

#Variables to Include in model (select from above list - varNames)
#VARS_TO_INCLUDE = ['inning', 'vis score', 'home score','erahome', 'eraAway', 'elo1pre', 'elo2pre', 'rating1_pre', 'rating2_pre', 'RS_home', 'RA_home','RS_away', 'RA_away']

#Model Parameters
HIDDEN_LAYERS = 2 # Number of Hidden Layers
NODES_PER_LAYER = 10 #Number of Nodes Per Layer
EPOCHS = 10 #How many Epochs (model training iterations)
BATCH_SIZE = 8 #How large of the 'batches' are for training data
ACTIVATION_FUNCTION = 'relu' #Activation function for neurons

##END MODEL SPECIFICATION##



# load the dataset
dataset = loadtxt('cleanUpScraped.csv', delimiter=',', skiprows = 1)

#Testing specific innings
#dataset2 = loadtxt('mergedDataReduced2.csv', delimiter=',', skiprows = 1)
#dataset5 = loadtxt('mergedDataReduced5.csv', delimiter=',', skiprows = 1)
#dataset8 = loadtxt('mergedDataReduced8.csv', delimiter=',', skiprows = 1)
 
#varIndexes = []
#start_time = time.time()

#for var in VARS_TO_INCLUDE:
#    varIndexes.append(varNames.index(var))
 
# split into input (X) and output (y) variables
X = dataset8[:,0:62]
y = dataset8[:,63]

#reduce variables

'''
test1gameInput = X[0,:]
print(test1gameInput)
print(X[0][1])
testarray = np.asarray(X[0:1])
print(testarray)
'''


#define model dimensions, functions, etc.
model = Sequential()
model.add(Dense(NODES_PER_LAYER, input_dim=len(VARS_TO_INCLUDE), activation=ACTIVATION_FUNCTION))
for i in range(1, (HIDDEN_LAYERS - 1)):
    model.add(Dense(NODES_PER_LAYER, activation=ACTIVATION_FUNCTION))
model.add(Dense(1, activation='sigmoid'))

#compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#fit model on this dataset
model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

# make class predictions with the model
#predictions = model.predict_classes(testarray)

print("--- %s seconds ---" % (time.time() - start_time))


# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")


'''
#testing for specific innings
#model.fit(X, y, validation_data=(X2,y2), epochs=15, batch_size=32)
#model.fit(X, y, validation_data=(X5,y5), epochs=15, batch_size=32)
#model.fit(X, y, validation_data=(X8,y8), epochs=15, batch_size=32)

'''
