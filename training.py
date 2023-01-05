from pymongo import MongoClient
import random
import os
import json
import pickle       # for serialization
import numpy as np
import csv
import pandas as pd
from time import strftime
from keras.callbacks import EarlyStopping
import nltk
from nltk.stem import WordNetLemmatizer     #verify the same word
# connect database
from db import train_table

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Dropout
from tensorflow.python.keras.optimizers import gradient_descent_v2

# get data from database
train_collection = train_table()

current_path = os.getcwd()
lemmatizer = WordNetLemmatizer()        #verify the same word

# intents = json.loads(open(current_path+'/chatbot/intents.json').read())       #Load file json

words = []          # All the words
classes = []        # All class 
documents = []      # all word with tag
ignore_letters = ['?', '!', '.', ',']       # all ignore letters

def check_sentence_exist(sentence):
    df = pd.read_csv(current_path+'/data/training_data.csv')
    
    # loop throw row
    for row in df.iterrows(): 
        if str(row[1]['Word list']) == str(sentence):
            return True
    return False

# # loop throw item in intents
# for intent in intents["intents"]:
#     for pattern in intent['patterns']:
#         word_list = nltk.word_tokenize(pattern)  # it look like split function ( 'what your name' => ['what', 'your','name'] )
#         words.extend(word_list)     # add to array words
#         documents.append((word_list, intent['tag']))   # add all word with tag to array documents
#         if not check_sentence_exist(word_list): # if not exist
#             with open(r'./data/training_data.csv', 'a') as f:       # Write data to file csv
#                 time = strftime('%H:%M:%S:%p, Date: %d/%m/%Y')
#                 writer = csv.writer(f)
#                 writer.writerow([f'{word_list}', f"{intent['tag']}", f'{time}'])
#         if intent['tag'] not in classes:
#             classes.append(intent['tag'])       # check if tag already have in classes and then add to array classes

# loop throw item in intents
for intent in train_collection.find():
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)  # it look like split function ( 'what your name' => ['what', 'your','name'] )
        words.extend(word_list)     # add to array words
        documents.append((word_list, intent['tag']))   # add all word with tag to array documents
        if not check_sentence_exist(word_list): # if not exist
            with open(current_path+'/data/training_data.csv', 'a') as f:       # Write data to file csv
                time = strftime('%H:%M:%S:%p, Date: %d/%m/%Y')
                writer = csv.writer(f)
                writer.writerow([f'{word_list}', f"{intent['tag']}", f'{time}'])
        if intent['tag'] not in classes:
            classes.append(intent['tag'])       # check if tag already have in classes and then add to array classes

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]        # remove ignore letter and same word
words = sorted(set(words))          # Sort

classes = sorted(set(classes))      # Sort

pickle.dump(words, open(current_path+'/data/words.pkl', 'wb'))      # Write word to file .pkl
pickle.dump(classes, open(current_path+'/data/classes.pkl', 'wb'))  # Write classes to file .pkl

training = []       # data to train
output_empty = [0] * len(classes)       # Array contain the number of elements is 0 equal to len(classes)

# loop throw item in documents
for document in documents:
    bag = []
    word_patterns = document[0]         # list word
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]      # lowercase 
    # loop throw word in words list
    for word in words:          
        bag.append(1) if word in word_patterns else bag.append(0)           # check if word exist in words

    output_row = list(output_empty)  # [0,0,0,...,0]
    output_row[classes.index(document[1])] = 1          # get index of intent
    training.append([bag, output_row])      # add to data
random.shuffle(training)        # shuffle data
training = np.array(training)   # Convert to numpy array    

train_x = list(training[:,0])      # X train
train_y = list(training[:,1])       # y train

# Create early stop when nothing change (in training process)
early_stopping = EarlyStopping(monitor='loss', patience=20, verbose=1)

# Create model (Dense neural network)
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))     # limit overfitting
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))     # limit overfitting
model.add(Dense(len(train_y[0]), activation='softmax'))

# optimizer
sgd = gradient_descent_v2.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# fit and save history
hist = model.fit(np.array(train_x), np.array(train_y), epochs=2000, batch_size=5, verbose=1,callbacks=early_stopping)   # training
model.save(current_path+'/data/chatbot_model.h5', hist)     # Save model
print("Done")


model.summary()
loss, acc = model.evaluate(train_x, train_y, verbose=1)
print('loss: ' + str(loss))
print('acc: ' + str(acc))

