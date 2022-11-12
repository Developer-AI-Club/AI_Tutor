#import natural language toolkit
import nltk
#using LancasterStemmer API
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#import numpy, tflearn, tensorflow, random and json
import numpy as np
import tflearn
import tensorflow
import random
import json

#the data for bot is in json file and need to open it with file
with open("data.json") as file:
    data = json.load(file)

#create some emty lists to append words
words = []
labels = []
docs_x = []
docs_y = []
mark = ["!","?"]

#read each intent  in intents of data.json (only 1 intent)
for intent in data["intents"]:
    #read each pattern sorted by pattern
    for pattern in intent["patterns"]:
        #split every words in pattern for execution
        words_need_tokenize = nltk.word_tokenize(pattern)
        #add to words
        words.extend(words_need_tokenize)
        #add words to doc_x
        docs_x.append(words)
        #add tag to doc_y
        docs_y.append(intent["tag"])

    #this step likes sorting the doc_y
    if intent["tag"] not in labels:
        labels.append((intent["tag"]))
#this step maybe not neccessary with the situation
words = [stemmer.stem(w.lower()) for w in words if w not in mark]
#order sorted words and labels
words = sorted(list(set(words)))
labels = sorted(labels)

#create data for training
training_bot_data = []
#create output
out = []
#0 for all elements appended to out_empty
out_empty = [0 for _ in range(len(labels))]
for x, doc in enumerate(docs_x):
    #create bag
    bag = []
    #split words in doc_x ( pattern element)
    wrds_stem_pattern = [stemmer.stem(w) for w in doc]
    for w in words:
        if w in wrds_stem_pattern:
            # append 1 to every words
            bag.append(1)
        else:
            #append 0 to every space
            bag.append(0)

    #make output line equal to 0 to every words in label length
    output_line = out_empty[:]
    #modify it somehow
    output_line[labels.index(docs_y[x])] = 1

    #bag = train_bot_data
    training_bot_data.append(bag)
    #out = output_line
    out.append(output_line)

#convert to numpy array for execution
training_bot_data = np.array(training_bot_data)
out = np.array(out)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training_bot_data[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(out[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)