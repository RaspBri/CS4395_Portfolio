# Source Credit for tensorflow skeleton code, I added the rest
# https://www.pycodemates.com/2021/11/build-a-AI-chatbot-using-python-and-deep-learning.html
import string
import nltk
nltk.download('punkt')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import tflearn
from tensorflow.python.framework import ops
import json
import pickle
import openai
import re, random
import spacy
nlp = spacy.load('en_core_web_sm')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import os

# REPLACE WHEN EXPIRES
key = "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"

filename = sys.argv[1]
print(filename)

with open(filename) as file:
    data = json.load(file)

train = input("Train the model type in (train): ")
# Data preprocessing start
if train.lower() == "train":
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])

        if intent["tag"] not in labels:
            labels.append(intent['tag'])

    # Getting rid of duplicate words
    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    '''
    Turning words into a bag of words.
    When feeding our model we want our words
    to be numeric instead of string value.
    So I'm going to do OHE the words turning
    them to numeric values.

    How we going to store it
    word list: ['a', 'am', 'be']
    OHE: [1, 0, 1]

    Put a 1 if that word exist else put a 0
    '''

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        # Bag of words
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        # Going through all the words
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        # Look through label list look for tag and set that output to 1
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    # turn them into arrays for easier model training
    training = np.array(training)
    output = np.array(output)

    with open((filename +'.data.pickel'), 'wb') as f:
        pickle.dump((words, labels, training, output), f)

else:
    with open((filename +'.data.pickel'), 'rb') as f:
        words, labels, training, output = pickle.load(f)
# Data preprocessing end

# Model creation start
ops.reset_default_graph()
# Input layer trying to get the length from none on
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 16, activation="relu")  # hidden layer
net = tflearn.fully_connected(net, 16, activation="relu")  # hidden layer
# Output layer solfmax
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
# end model creation


# Start training
'''
training = input values
output = output values
n_epoch = how many times do I want to train same dataset
batch_sizes = how many samples of data will pass through at a time 
show_metric = Makes the output look nicer
'''

if train.lower() == "train":
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")

else:
    model.load("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words if word not in "?"]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def perform_lemmatization(tokens):
    return [stemmer.stem(token) for token in tokens]


def get_processed_text(doc):
    return perform_lemmatization(nltk.word_tokenize(doc.lower().translate((dict((ord(punctuation), None) for punctuation in string.punctuation)))))

def generate_response(user_input, responses):
    bot_response = ''
    responses.append(user_input)

    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(responses)
    similar_vector_vals = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_num = similar_vector_vals.argsort()[0][2]

    matched_vector = similar_vector_vals.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        print("cannot understand")
    else:
        print(responses[similar_sentence_num])


def add_likes(likes_list):
    data["intents"].append({
        "tag": "likes",
        "patterns": ["I like", "I love", "I enjoy", "favorite"],
        "responses": likes_list
    })

def add_dislikes(dislikes_list):
    data["intents"].append({
        "tag": "dislikes",
        "patterns": ["I don't like", "I do not like","I hate", "I don't enjoy", "I do not enjoy", "least favorite"],
        "responses": dislikes_list
    })

def use_openai(mood):
    openai.api_key = key
    model_engine = "gpt-3.5-turbo"

    # Use ChatGPT to get relevant wiki links about the user's interest
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": ("what are some phrases someone who is {} would say. Play the role of a hard worker with these emotions".format(mood))}
          ]
    )
    message = response.choices[0].message.content
    message = re.findall(r'"([^"]*)"', message)
    print(message)
    return message


def choose_mood(number):
    if number == 1:
        mood = 'happy'
    elif number == 2:
        mood = 'mad'
    elif number == 3:
        mood = 'sad'
    elif number == 4:
        mood = 'mockery'
    else:
        mood = 'neutral'
    return mood

def sentiment(text):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(text)

    #print("Overall sentiment dictionary is : ", sentiment_dict)
    #print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    #print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    #print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    #print("Sentence Overall Rated As", end=" ")

    return sentiment_dict['neg'], sentiment_dict['neu'], sentiment_dict['pos']

def mock(user_input):
    inp = list(user_input.lower())
    for x in range(len(inp)):
        if x % 2 == 0:
            inp[x] = inp[x].lower()
        else:
            inp[x] = inp[x].upper()

    inp = ''.join(inp)
    print(inp)

def user_checkin(user_fun_rating):
    vader_neg, vader_neu, vader_pos = sentiment(user_fun_rating)

    # decide sentiment as positive, negative and neutral
    if vader_pos >= 0.05:
        #print("Positive")
        mood = 1
    elif vader_neg >= 0.05:
        #print("Negative")
        mood = random.randint(2, 4)
    else:
        #print("Neutral")
        mood = 5

    mood = choose_mood(mood)
    message_list = use_openai(mood)

    if mood == 'mockery':
        mock(user_fun_rating)
    print(random.choice(message_list))


def extract_clauses(text):
    sentences = nltk.sent_tokenize(text)
    clauses = []

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        clauses_tags = []
        for i, (word, tag) in enumerate(pos_tags):
            if tag in ('IN', 'DT', 'TO', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):  # get verb phrase tags
                if i > 0 and pos_tags[i - 1][1] not in ('IN', 'DT', 'TO', 'CC'):  # omit tags
                    clauses.append(' '.join(clauses_tags))
                    clauses_tags = []
                clauses_tags.append(word)  # add to clause_tag list
            else:
                clauses_tags.append(word)
        clauses.append(' '.join(clauses_tags))  # add to clause tag list
    clauses = extract_clauses(text)
    clauses = [''.join(x) for x in zip(clauses[0::2], clauses[1::2])]
    #print(clauses)
    if len(clauses) > 1:
        return True
    else:
        return False

# Generate user input
def chat():
    # user input
    print("Start talking with bot!(type 'quit' to stop)")
    likes_list = []
    dislikes_list = []
    chat_count = 0

    while True:

        inp = input("You: ")
        if inp.lower() == "quit":
            break
        if chat_count == 5:
            print("Are you having fun?")
            user_fun_rating = input("You: ")
            user_checkin(user_fun_rating)

            print("Are you ready to get back to learning? (y/n)")
            learn_again = input("You: ")
            if learn_again == 'y':
                print("Let's get back to learning.")
            elif learn_again == 'n':
                print("What would you rather do?")
                user_fun_rating = input("You: ")
                user_checkin(user_fun_rating)
                print("Let's get back to learning.")
            chat_count = 0

        elif 'dislike' in inp:
            dislike = inp
            dislike = dislike.rsplit('dislike ', 1)[1]
            dislikes_list.append(dislike)
            print("I see")
        elif 'like' in inp:
            like = inp
            like = like.rsplit('like ', 1)[1]
            likes_list.append(like)
            print("I enjoy {} too".format(like))

        else:
            # All this is going to give us a matrix of numbers where the numbers are probabilities of each class
            results = model.predict([bag_of_words(inp, words)])
            # Argmax will grab the index of largest probability in the matrix
            results_index = np.argmax(results)
            tag = labels[results_index]

            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            # get most accurate response
            tfidf_vectorizer = TfidfVectorizer()
            sparse_matrix = tfidf_vectorizer.fit_transform(responses)
            doc_term_matrix = sparse_matrix.toarray()

            tgt_transform = tfidf_vectorizer.transform([inp]).toarray()
            tgt_cosine = cosine_similarity(doc_term_matrix, tgt_transform)
            tgt_cosine_list = list(tgt_cosine)
            i = tgt_cosine_list.index(max(tgt_cosine_list))
            print(responses[i])

            text = responses[i]
            cmd = "python clauses.py \"{}\"".format(responses[i]) # get clauses
            os.system(cmd)

        chat_count += 1

    # add to .json file with likes and dislikes
    if len(likes_list) > 0:
        add_likes(likes_list)
        with open(filename, 'w') as outfile: # Write the updated object back to the file
            json.dump(data, outfile, indent=4)

    if len(dislikes_list) > 0:
        add_dislikes(dislikes_list)
        with open(filename, 'w') as outfile: # Write the updated object back to the file
            json.dump(data, outfile, indent=4)


chat()
