import nltk
# nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import openai
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
openai.api_key = "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"
from tensorflow.python.framework import ops
import numpy as np
import tflearn
import random
import json
import pickle
import wikipedia



with open("D:\CODE\Python\Python\ChatBot\intents2.json") as file:
    data = json.load(file)

try:  
    with open("data.pkl", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:  
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])
            
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
                
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)
        
    training = np.array(training)
    output = np.array(output)

    with open("data.pkl", "wb") as f:
        pickle.dump((words, labels, training, output), f)
        
ops.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch = 1000, batch_size = 8, show_metric = True)
    model.save("model.tflearn")
        
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return np.array(bag)

def summarize_text(text, num_sentences):
      parser = PlaintextParser.from_string(text, Tokenizer("english"))

      summarizer = LexRankSummarizer()

      summary = summarizer(parser.document, num_sentences)

      return [str(sentence) for sentence in summary]

def chat():
    responses = None
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]
        
        if results[results_index] > 0.5:
        
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                        
            print("Bot:",random.choice(responses))
        else:
            responses = "I don't know"
            if responses == "I don't know":
                prompt = f"Summarize the Wikipedia page for {inp}"
                openai_response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=3500,
                    temperature=0.5,
                    top_p=1.0,
                )
                summary = openai_response["choices"][0]["text"]
                responses = summarize_text(summary, 7)
            print(responses)
            
            
      
                
# chat()
