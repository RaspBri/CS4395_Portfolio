# Use ChatGPT to get website links relating to the topic the user wants to discuss
# Use links for webscraping to build corpus for chatbot
"""import openai

openai.api_key = "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"
model_engine = "gpt-3.5-turbo"

# Get user input for topic to discuss
topic = "houseplants"

# Use ChatGPT to get relevant wiki links about the user's interest
response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": ("Get 20 wikipedia links that tell me about " + topic)}
      ]
)
message = response.choices[0].message.content
file = open("links.txt", "a")
file.write(message)
file.close()
#print(str(message))

                                                    # Save jokes for later
response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": ("Tell me some jokes about " + topic)}
      ]
)
"""
import string

"""
To fix "unresolved reference" error for sklearn, run this command >>> pip install -U scikit-learn

Run command in terminal before running >>> pip install nltk tensorflow tflearn
INstall >>> pip install jsbeautifier
"""
import re
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import math
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json
import jsbeautifier
import pickle


#
def write_to_file(soup):
    for paragraph in soup.find_all('p'):
        text = ''
        text += paragraph.text
        text = re.sub(r'\[\d+\]', '', text)  # remove mini reference numbers from lines
        f = open((URL.rsplit('/', 1)[-1]) + '.txt', "a") # read page name from URL
        f.write(text)


#
def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc.lower().replace('\n', ' ').replace(',', ' '))
    tokens = [t for t in tokens if t.isalpha() and t.lower() and
              t not in stopwords.words('english')]

    sentence = sent_tokenize(doc)

    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict, sentence


#
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    term_weight = sorted(tf.items(), key=lambda x: x[1], reverse=True)
    return term_weight


#
def term_freq():
    vocab = set()  # set of words
    tf_dict_list = []
    idf_dict = {}
    all_words = []  # contains tf_dict.keys()
    term_weight_list = []  # tf_idf for each file
    sentences = []

    # get tf_dict for each file
    for item in file_names:
        file_contents = open(item, 'r')
        tf_dict, sentence = create_tf_dict(file_contents.read())
        vocab = vocab.union(set(tf_dict.keys()))  # make set of all unique words
        all_words += tf_dict.keys()  # get all words from every file
        tf_dict_list.append(tf_dict)
        sentences += sentence

    for term in vocab:  # get idf
        temp = ['x' for voc in all_words if term in voc]
        idf_dict[term] = math.log((1 + len(file_names)) / (1 + len(temp)))

    for item in range(len(file_names)):
        term_weight = (create_tfidf(tf_dict_list[item], idf_dict))
        term_weight_list.append(term_weight)

    return vocab, tf_dict_list, idf_dict, all_words, term_weight_list, sentences


#
def add_intents(tag, temp_list, word_list):
    count = 5
    if len(word_list) < 5:
        count = 3

    top = []
    for item in word_list: # get top 5 words w/ frequencies
        top.append(item[0])
    # Need to just get word not probability with word

    data["intents"].append({
        "tag": "{}".format(tag),  # get word to make the tag
        "patterns": top,
        "responses": temp_list.split('.')
    })


#
def add_defaults():
    data["intents"].append({
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey"],
                "responses": ["Hi", "Hello", "Hey", "Good to see you"],
                "context":[""]
    })
    data["intents"].append({
                "tag": "goodbye",
                "patterns": ["Bye", "Goodbye", "See you later"],
                "responses": ["Nice chatting, bye", "Bye", "Goodbye"],
                "context": [""]
    })
    data["intents"].append({
                "tag": "thanks",
                "patterns": ["Thanks", "Thank you"],
                "responses": ["You're Welcome", "No problem"],
                "context": [""]
    })


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Read in links to files about user's interest
    file = open("links.txt", "r")

    # Get URLs from .txt file and save them to their own file
    file_names = []
    data = {"intents": []}

    for line in file:
        URL = (re.search("(?P<url>https?://[^\s]+)", line).group("url"))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        file_names.append((line.rsplit('/', 1)[-1]).strip() + ".txt")
        #write_to_file(soup)                                                       # <= BE SURE TO MAKE LINE VISIBLE

    vocab, tf_dict_list, idf_dict, all_words, term_weight_list, sentences = term_freq()
    """
    to traverse through most frequent words
    term_weight_list[x] where x is the document index you wish to see
    """

    # Make contents for .json file
    temp_list = ''
    for count in range(len(file_names)): # get to file
        for i in range(len(term_weight_list[count])): # go through all words from term weight
            for sentence in sentences: # get to sentence level
                if term_weight_list[count][i][0] in sentence: # if word is found in sentence
                    temp_list += sentence # add sentence to a list
        word_list = (sorted(tf_dict_list[count].items(), key=lambda x: x[1], reverse=True))
        add_intents(term_weight_list[count][i][0], temp_list, word_list[:5]) # add list of sentences to .json
        temp_list = '' # clear list for next run


    # write dict to .json
    add_defaults()  # add default values to .json file

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


