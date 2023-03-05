import pickle
import nltk
from nltk import word_tokenize


# Read, remove new lines, make unigram, make bigrams
def processText(file):
    clean_file = file.read().replace('\n', '') # Read & Remove new lines
    unigrams = word_tokenize(clean_file) # tokenize text to a unigram
    bigrams = [(unigrams[k], unigrams[k + 1]) for k in range(len(unigrams) - 1)] # make bigram
    return unigrams, bigrams

# preprocess text, create unigram & bigram dictionary
def runProgram1(filename):
    file = open(filename, "r")
    unigrams, bigrams = processText(file)  # Read & Remove new lines
    bigramDictionary = {t: bigrams.count(t) for t in set(bigrams)} # Bigram dictionary [‘token1 token2’] -> count
    unigramDictionary = {t: unigrams.count(t) for t in set(unigrams)} # Unigram dictionary [‘token1’] -> count

    return unigramDictionary, bigramDictionary

# create unigram & bigram pickle file
def pickleDictionary(unigramDict, bigramDict, filename):
    pickle.dump(unigramDict, open((filename + '_unigramDict.pickle'), 'wb')) # pickle unigram
    pickle.dump(bigramDict, open((filename + '_bigramDict.pickle'), 'wb')) # pickle bigram

if __name__ == '__main__':

    unigramDictionary1, bigramDictionary1 = runProgram1("LangId.train.English")
    pickleDictionary(unigramDictionary1, bigramDictionary1, "LangId.train.English")

    unigramDictionary2, bigramDictionary2 = runProgram1("LangId.train.French")
    pickleDictionary(unigramDictionary2, bigramDictionary2, "LangId.train.French")

    unigramDictionary3, bigramDictionary3 = runProgram1("LangId.train.Italian")
    pickleDictionary(unigramDictionary3, bigramDictionary3, "LangId.train.Italian")
