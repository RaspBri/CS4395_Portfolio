import requests
import math
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize, ngrams, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

""" 
            MUST HAVE FEW LINKS FROM OUTSIDE THE DOMAIN (GO FOR SOCIAL MEDIA PAGES)
            - maybe global variable for the range?
            - update all variableLikeThis to variable_like_this
"""

def scrapeText(URL, count):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    for p in soup.select('p'):
        file = open(('link' + str(count) + '.txt'), "a")
        file.write(p.get_text())
        #print(p.get_text())


def cleanText():
    # remove newlines
    text_no_line_breaks = ''
    for i in range(1, 15):
        file = open('link' + str(i) + '.txt')
        for eachLine in file:
            stripped_line = eachLine.rstrip('\t\n')
            text_no_line_breaks += stripped_line


def tokenizeSentences():
    for i in range(1, 15):
        file = open('link' + str(i) + '.txt').read()
        # tokenize sentences and lowercase
        tokens = sent_tokenize(file.lower())
        # write tokens to new file
        outFile = open(('link' + str(i) + 'tokens.txt'), "w")
        #print(tokens)
        outFile.writelines(tokens)


def tokenizeWords():
    wordList = []
    for i in range(1, 15):
        file = open('link' + str(i) + 'tokens.txt').read() # read sentences in as tokens
        tokens = word_tokenize(file) # break up sentences into tokens of words
        # tokenize words by removing stop words, punctuation, and lowercase everything
        tokens = [t for t in tokens if t.isalpha() and t.lower() and
                  t not in stopwords.words('english')]
        for t in tokens:
            wordList.append(t)

        """ Surprising how few words made it through to be saved into the .txt file """

        outFile = open(('link' + str(i) + 'tokens.txt'), "w")
        for item in tokens:
            outFile.write(item) # write string of tokens to .txt file
            outFile.write("\n")

    wordList = list(set(wordList))
    return wordList

def findTermFreq():
    listDict = []
    for i in range(1, 15):
        tfDict = {}
        # read all strings from file
        with open(('link' + str(i) + 'tokens.txt'), "r") as f:
            text = f.read()
        tokens = word_tokenize(text) # tokenize text from each file

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
        #print(list(tfDict.values())[2])
        #print(tfDict.values()) # print entire range of dict values for terms
    return listDict


def findInverseDocFreq(tfDict, vocList):
    urlVoc = []
    idfDict = {}

    # take list of words from each dict in tfDict and put into list
    for item in tfDict:
        urlVoc.append(item.keys())

    #for term in allVoc
    for term in vocList:
        temp = ['x' for voc in urlVoc if term in voc]
        idfDict[term] = math.log((1 + 14) / (1 + len(temp)))
        #print(idfDict[term])
    #print(idfDict)
    return idfDict


def create_tfidf(tf, idf):
    # tf = dictionary from page
    # idf = single dictionary all unique words from every page
    tf_idf = {}
    for t in tf.keys():
       tf_idf[t] = tf[t] * idf[t]
    #term_weight = sorted(tf.items(), key = lambda x:x[1], reverse = True) # highest tf-idf
    term_weight = sorted(tf.items(), key = lambda x:x[1]) # lowest tf-idf // terms are more frequent
    # print(len(tf_idf))
    return tf_idf, term_weight


if __name__ == '__main__':
    # Topic = Plants
    # Website, Texas Tulips
    # Small local plant shops did not have enough URLs for the project, using this website instead
    URL = 'https://texas-tulips.com/?utm_source=local&utm_medium=organic&utm_campaign=gmb'

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    #text = soup.get_text()
    #print(text[:100]) # Outputs headers only

    #for p in soup.select('p'):
   #     print(p) # print paragraph info

    # Loop to find all URLs on Texas Tulips' website
    counter = 0
    for link in soup.find_all('a'):
        counter += 1
        if counter > 15:
            break
        scrapeText(link.get('href'), counter)

    cleanText() # remove newlines
    tokenizeSentences() # make everything lowercase
    vocList = tokenizeWords() # remove stopwords & punctuation, return list of unique words
    tfDict = findTermFreq() # return term frequency as list with dictionaries for each page
    idfDict = findInverseDocFreq(tfDict, vocList) # return inverse document frequency

    # iterate through all term freq dicts for each page
    for i in range(len(tfDict)):
        tf_idf, termWeights = create_tfidf(tfDict[i], idfDict) # tf-idf value
        #print(tf_idf) # print all terms from each page
        print(termWeights[:25]) # print top 25 words from page
    
    """
    TOP 10 TERMS:
    tulips, dallas, texas, season, contact,
    february, april, visit, times, pay, parking
    """
    
    knowledgeBase = {
        'tulips': ['Tulips come in many colors such as: purple, red, orange, yellow, white, and pink', 
                 'Tulip Care: Cut stems and place in fresh water'],
        'dallas': ,
        'texas': ,
        'season': ,
        'contact': ['Address: North of Dallas at 10656 FM2931, Pilot Point TX 76258', 
                  'Email: info@texas-tulips.com', 'Phone: 940-440-0232'],
        'february': ,
        'april': ,
        'visit': ,
        'times': , 
        'pay': ['Accepted forms of payment: Visa, MasterCard, and Cash'], 
        'parking': 
    }
