import requests
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize

def scrapeText(URL, count):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    for p in soup.select('p'):
        file = open(('link' + str(count) + '.txt'), "a")
        file.write(p.get_text())
        #print(p.get_text())


def cleanText():
    text_no_line_breaks = ''
    for i in range(1, 15):
        file = open('link' + str(i) + '.txt')
        for eachLine in file:
            stripped_line = eachLine.rstrip('\t\n')
            text_no_line_breaks += stripped_line


def tokenizeSentences():
    for i in range(1, 15):
        file = open('link' + str(i) + '.txt').read()
        tokens = sent_tokenize(file)
        outFile = open(('link' + str(i) + 'tokens.txt'), "w")
        #print(tokens)
        outFile.writelines(tokens)


def findTerms():
    


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

    cleanText()
    tokenizeSentences()
    
