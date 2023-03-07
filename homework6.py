import requests
import math
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize, ngrams, FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

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

        listDict.append(tfDict) # add to list for each file
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
    #print(tf) # list of dictionaries from each file
    #print(idf) # single dictionary all unique words
    #tf_idf = {key: tf[key] * idf.get(key, 0) for key in tf}
    #print((tf[3]).keys())
    #print(list(tf[5].values())[5])
    #print(list(idf.values())[6])
    tf_idf = {}
    #print(type(list((tf[4]).values())[5]))
    #print(((list(idf.values())[4])))
    for i in range(15): # go through all files
        for t in (tf[i]): # go through all dictionaries in tf
            for x in (tf[i]).values(): # go through all values in dictionary
                tf_idf[t] = (list((tf[t]).values())[x]) * (list(idf.values())[x])
            print(tf_idf[t])
            
    #print(tf_idf)


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
    tfDict = findTermFreq()
    idfDict = findInverseDocFreq(tfDict, vocList) # return idfDict
    create_tfidf(tfDict, idfDict)
