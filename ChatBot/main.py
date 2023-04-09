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

import re
import requests
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
import math


def write_to_file(soup):
    for paragraph in soup.find_all('p'):
        text = ''
        text += paragraph.text
        text = re.sub(r'\[\d+\]', '', text)  # remove mini reference numbers from lines
        f = open((URL.rsplit('/', 1)[-1]) + '.txt', "w") # read page name from URL
        f.write(text)


def create_tf_dict(doc):
    tf_dict = {}
    tokens = word_tokenize(doc.lower().replace('\n', ' ').replace(',', ' '))
    tokens = [t for t in tokens if t.isalpha() and t.lower() and
              t not in stopwords.words('english')]
    print(tokens)
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

    return tf_dict

# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Read in links to files about user's interest
    file = open("links.txt", "r")
    # print(file.read())

    # Get URLs from .txt file and save them to their own file
    file_names = []
    for line in file:
        URL = (re.search("(?P<url>https?://[^\s]+)", line).group("url"))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        file_names.append((line.rsplit('/', 1)[-1]).strip() + ".txt")
    write_to_file(soup)

    vocab = set()  # set of words
    # lowercase text, remove newlines
    for item in file_names:
        file_contents = open(item, 'r')
        tf_dict = create_tf_dict(file_contents.read())
        vocab = vocab.union(set(tf_dict.keys()))
        #print(tf_dict)
    #print("number of unique words:", len(vocab))



