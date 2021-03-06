import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open("/home/app/intents.json") as file:
    data = json.load(file)

try:
    with open("/home/app/data.pickle", "rb") as f:
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

    words = [stemmer.stem(w.lower()) for w in words if w not in '?']
    words = sorted(list(set(words)))

    labels.sort()

    training = []
    output = []
    out_empty = [0 for i in range(len(labels))]

    for index, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for word in words:
            if word in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[index])] = 1
        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    with open("/home/app/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])] if len(training) else 0)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]) if len(output) else 0, activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# try:
#     model.load("model.tflearn")
# except:
if True:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("/home/app/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for i in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(w.lower()) for w in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


def chat():
    print("Start talking with the bot!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            print("Exiting chat bot")
            break
        results = model.predict([bag_of_words(inp, words)])
        if max(list(results[0,:]))<0.6:
            print("I don't understand. Can you be clear?")
            continue
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        responses = []
        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["responses"]
        print(random.choice(responses))


chat()
