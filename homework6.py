import requests
import math
from bs4 import BeautifulSoup
import pickle
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

""" 
            Some links go to facebook / instagram
            Topic: Plants :)
            Website: Texas Tulips
"""

# Go through given url and save text to .txt file
def scrapeText(URL, count):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    for p in soup.select('p'):
        file = open(('link' + str(count) + '.txt'), "a")
        file.write(p.get_text())


# remove newlines and tabs from .txt files
def cleanText():
    textNoLineBreaks = ''
    for i in range(1, 15):
        file = open('link' + str(i) + '.txt')
        for eachLine in file:
            stripped_line = eachLine.rstrip('\t\n')
            textNoLineBreaks += stripped_line


# tokenize sentences from each .txt file and save to new file ending w/ tokens.txt
def tokenizeSentences():
    for i in range(1, 15):
        file = open('link' + str(i) + '.txt').read()
        tokens = sent_tokenize(file.lower()) # tokenize sentences and lowercase
        outFile = open(('link' + str(i) + 'tokens.txt'), "w") # write tokens to new file
        outFile.writelines(tokens)

# tokenize words by removing stopwords, punctuation, and lowercase everything
def tokenizeWords():
    wordList = []
    for i in range(1, 15):
        file = open('link' + str(i) + 'tokens.txt').read()
        tokens = word_tokenize(file) # break up sentences into tokens of words
        tokens = [t for t in tokens if t.isalpha() and t.lower() and
                  t not in stopwords.words('english')]
        for t in tokens:
            wordList.append(t) # add tokens from each sentence to list

        """ Surprising how few words made it through """

        outFile = open(('link' + str(i) + 'tokens.txt'), "w")
        for item in tokens:
            outFile.write(item) # write string of tokens to .txt file
            outFile.write("\n")

    wordList = list(set(wordList)) # get only unique words from tokenized text
    return wordList


# Term Frequency for each page from .txt file. Must convert strings to tokens again
def findTermFreq():
    listDict = []
    for i in range(1, 15):
        tfDict = {}
        with open(('link' + str(i) + 'tokens.txt'), "r") as f:
            text = f.read()
        tokens = word_tokenize(text) # tokenize text from each file b/c it was saved as a string

        # go through all tokens and calculate term frequency for each word
        for word in tokens:
            if word in tfDict:
               tfDict[word] += 1
            else:
                tfDict[word] = 1

        # normalize the term frequency by number of tokens
        for word in tfDict.keys():
            tfDict[word] = tfDict[word] / len(tokens)

        listDict.append(tfDict) # add to list for each page
    return listDict


# Find Inverse Document Frequency for each page (AKA how often the word appears across all pages)
# IDF = log(total number of documents in corpus) / (number of documents in corpus that contain term)
def findInverseDocFreq(tfDict, vocList, numDocs):
    urlVoc = []
    idfDict = {}

    # take list of words from each dict in tfDict and put into list
    for item in tfDict:
        urlVoc.append(item.keys())

    for term in vocList:
        temp = ['x' for voc in urlVoc if term in voc]
        idfDict[term] = math.log((1 + numDocs) / (1 + len(temp))) # adding 1 to prevent diving by 0
    return idfDict


# tf-idf shows importance of a term for a page in the corpus
def create_tfidf(tf, idf):
    """
        tf = dictionary from page
        idf = single dictionary all unique words from every page
        td-idf closer to 0 = less important
    """

    tf_idf = {}
    for t in tf.keys():
       tf_idf[t] = tf[t] * idf[t]

    term_weight = sorted(tf.items(), key = lambda x:x[1], reverse = True) # highest tf-idf
    # term_weight = sorted(tf.items(), key = lambda x:x[1]) # lowest tf-idf
    return tf_idf, term_weight


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    # Smaller local plant shops did not have enough URLs for the project, using this website instead
    URL = 'https://texas-tulips.com/?utm_source=local&utm_medium=organic&utm_campaign=gmb'

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Loop to find all URLs on Texas Tulips' website
    counter = 0
    urlList = []
    for link in soup.find_all('a'):
        counter += 1
        if counter > 20: # get 20 urls
            break
        urlList.append(link.get('href'))
    urlList = list(set(urlList)) # get only unique urls
    numDocs = len(urlList) # will be used in findInverseDocFreq()

    for i in range(1, (len(urlList) + 1), 1): # range(start, stop, step)
        scrapeText(link.get('href'), i) # scrape each url for text


    cleanText() # remove newlines
    tokenizeSentences() # make everything lowercase
    vocList = tokenizeWords() # remove stopwords & punctuation, return list of unique words
    tfDict = findTermFreq() # return term frequency as list with dictionaries for each page
    idfDict = findInverseDocFreq(tfDict, vocList, numDocs) # return inverse document frequency

    # iterate through all term freq dicts for each page
    for i in range(len(tfDict)):
        tf_idf, termWeights = create_tfidf(tfDict[i], idfDict) # tf-idf value
        #print(tf_idf) # print all terms from each page
    print(termWeights[:25]) # print top 25 words from page


    """
    TOP 10 TERMS:
    tulips, dallas, texas, spring, contact,
    picking, april, visit, field, activities, parking
    """

    # mini knowledge base w/ basic facts to build out later
    # I think the word season should be there
    knowledgeBase = {
        'tulips': ['Tulips come in many colors such as purple, red, orange, yellow, white, and pink',
                   'Tulip Care: Cut stems and place in fresh water',
                   'There are 100 varieties of tulips on the grounds'
                ],
        'dallas': ['Address: North of Dallas at 10656 FM2931, Pilot Point TX 76258'
                ],
        'texas': ['Address: North of Dallas at 10656 FM2931, Pilot Point TX 76258'
                ],
        'spring': ['Open Season: During end of winter and early spring',
                   'Open during February, March, and mid April'
                ],
        'contact': ['Address: North of Dallas at 10656 FM2931, Pilot Point TX 76258',
                  'Email: info@texas-tulips.com',
                  'Phone: 940-440-0232',
                  'Bulb planting services. Email/Call for a quote.'
                ],
        'picking': ['Open Season: During end of winter and early spring',
                    'You may pick tulips for $2.50/stem. All tulips will be wrapped and put in flower gel',
                    'Picking baskets are provided on the field'
                ],
        'april': ['Open Season: During end of winter and early spring',
                  'End Season: Mid April'
                ],
        'visit': ['Hours: 10AM - 8PM Everyday',
                  'Address: North of Dallas at 10656 FM2931, Pilot Point TX 76258',
                  'Free parking'
                ] ,
        'field': ['Hours: 10AM - 8PM Everyday',
                  'Dogs are NOT allowed in the field',
                  'Picnic tables and restrooms available',
                  'No drones allowed'
                ],
        'accept': ['Tulip Picking Entrance Fee: $5/person',
                   'Discounts for Veterans and Seniors: $7.50/person (includes three tulips & only during the week on business days)',
                    'Accepted forms of payment: Visa, MasterCard, and Cash',
                   'On Site Cafe',
                   'Professional photographers allowed for $25 entrance fee and $5 per client'
                ],
        'parking': ['Parking Fee: FREE'
                ]
    }

    pickle.dump(knowledgeBase, open('knowledgeBase.pickle', 'wb')) # pickle database
