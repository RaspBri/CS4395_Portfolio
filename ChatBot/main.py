# Use ChatGPT to get website links relating to the topic the user wants to discuss
# Use links for webscraping to build corpus for chatbot
import openai
import re
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import json
import os
import math
import random



"""
To fix "unresolved reference" error for sklearn, run this command >>> pip install -U scikit-learn
Run command in terminal before running >>> pip install nltk tensorflow tflearn
Install >>> pip install jsbeautifier
"""

# REPLACE WHEN EXPIRES
key = "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"


def use_openai(topic):
    openai.api_key = key
    model_engine = "gpt-3.5-turbo"

    # Use ChatGPT to get relevant wiki links about the user's interest
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": ("Get 10 wikipedia links that tell me about " + topic)}
          ]
    )
    message = response.choices[0].message.content
    file = open("links.txt", "a")
    file.write(message)
    file.close()




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
    data["intents"].append({
        "tag": "{}".format(tag),  # get word to make the tag
        "patterns": word_list,
        "responses": temp_list.split('.')
    })


#
def add_defaults(name):
    data["intents"].append({
        "tag": "thanks",
        "patterns": ["Thanks", "Thank you"],
        "responses": ["You're Welcome", "No problem"]
    })
    data["intents"].append({
        "tag": "mood",
        "patterns": ["How are you?", "What's up?"],
        "responses": ["I am a bot."]
    })
    data["intents"].append({
        "tag": "agree",
        "patterns": ["Yes", "Yea", "Sure", "Ok"],
        "responses": ["Awesome!", "Love to hear it!"]
    })
    data["intents"].append({
        "tag": "disagree",
        "patterns": ["No", "Never", "Eww", "Nah"],
        "responses": ["Oh, my bad.", "Apologies."]
    })
    data["intents"].append({
        "tag": "goodbye",
        "patterns": ["Bye", "Goodbye", "See you later"],
        "responses": ["Nice chatting, bye", "Bye, {}".format(name), "Goodbye, {}".format(name)]
    })
    data["intents"].append({
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey"],
        "responses": ["Hi, {}!".format(name), "Hello", "Hey", "Good to see you, {}".format(name)]
    })

# skip over duplicate words adn omit the word "also"
def check_list(word_list, seen):
    final_list = []
    for word in word_list:
        count = seen.count(word[0])
        if count < 1 and word[0] != 'also':
            final_list.append(word[0])
            seen.append(word[0])
    return final_list, seen


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    data = {"intents": []}

    print("Please enter your name...")
    name = input("You: ")

    # validate user
    if os.path.isfile('{}_data.json'.format(name)):
        print("Hi, {}".format(name))
        cmd = "python extractions.py {}_data.json".format(name)

        responses = []
        for tg in data["intents"]:
            if tg['tag'] == 'likes':
                responses = tg['responses']
        if len(responses) > 1: # if you previously told a like and dislike
            likes = random.choice(responses)
            print("Welcome back! I remember last time you said you liked {}, did you get around to that after we chatted?".format(likes))
        os.system(cmd)
    else:
        # get topic from user
        print("What is your favorite hobby? ")
        hobby = input("You: ")

        use_openai(hobby) # get links and save to .txt file
        print("Ok, I will learn about this...please wait")
        # Read in links to files about user's interest
        file = open("links.txt", "r")

        # Get URLs from .txt file and save them to their own file
        file_names = []


        for line in file:
            URL = (re.search("(?P<url>https?://[^\s]+)", line).group("url"))
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            file_names.append((line.rsplit('/', 1)[-1]).strip() + ".txt")
            write_to_file(soup)
        vocab, tf_dict_list, idf_dict, all_words, term_weight_list, sentences = term_freq()

        """
        to traverse through most frequent words
        term_weight_list[x] where x is the document index you wish to see
        """

        # Make contents for .json file
        temp_list = ''
        seen_list = []
        for count in range(len(file_names)): # get to file
            for i in range(len(term_weight_list[count])): # go through all words from term weight
                for sentence in sentences: # get to sentence level
                    if term_weight_list[count][i][0] in sentence: # if word is found in sentence
                        temp_list += sentence # add sentence to a list
            word_list = (sorted(tf_dict_list[count].items(), key=lambda x: x[1], reverse=True))
            word_list, seen_list_add = check_list(word_list, seen_list)
            seen_list.append(seen_list_add)
            add_intents(term_weight_list[count][i][0], temp_list, word_list[:5]) # add list of sentences to .json
            temp_list = '' # clear list for next run

        # write dict to .json
        add_defaults(name.lower())  # add default values to .json file

        with open('{}_data.json'.format(name), 'w') as outfile:
            json.dump(data, outfile, indent=4)

        # get special filename
        cmd = "python extractions.py {}_data.json".format(name)
        os.system(cmd)
