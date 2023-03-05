# NGram Model Program 2
import sys
import re
import pickle
from nltk.util import ngrams
from nltk import word_tokenize


def compute_prob(text, unigram_dict, bigram_dict, V):
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    p_laplace = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((b + 1) / (u + V))

    return p_laplace


def checkSol(outputs):
    correct = 0
    file = open('LangId.sol', 'r')
    for i, item in enumerate(file):
        print("Guess: ", outputs[i])
        if outputs[i] == item:
            print("The calculation was CORRECT! It was ", item)
            correct += 1
        else:
            print("The calculation was INCORRECT! It was ", item)
    print("The percentage of correctly classified instances is: ", (correct / len(outputs)))
    print("Correct: ", correct, " Incorrect: ", (len(outputs) - correct))


if __name__ == '__main__':
    # sysarg for 6 unigram and bigram files in 'data'
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # read in pickled dictionaries
    english_unigram_dict = pickle.load(open('LangId.train.English_unigramDict.pickle', 'rb'))
    french_unigram_dict = pickle.load(open('LangId.train.French_unigramDict.pickle', 'rb'))
    italian_unigram_dict = pickle.load(open('LangId.train.Italian_unigramDict.pickle', 'rb'))

    english_bigram_dict = pickle.load(open('LangId.train.English_bigramDict.pickle', 'rb'))
    french_bigram_dict = pickle.load(open('LangId.train.French_bigramDict.pickle', 'rb'))
    italian_bigram_dict = pickle.load(open('LangId.train.Italian_bigramDict.pickle', 'rb'))

    # read in each line of test file
    text = open('LangId.test', 'r')
    tokens = text.readlines()

    # list of languges guessed from calculations
    outputs = []

    line = 1
    # calculate probabilty for each language for each sentence
    for t in tokens:
        eng = compute_prob(t, english_unigram_dict, english_bigram_dict, len(english_unigram_dict))
        ita = compute_prob(t, italian_unigram_dict, italian_bigram_dict, len(italian_unigram_dict))
        fre = compute_prob(t, french_unigram_dict, french_bigram_dict, len(french_unigram_dict))

        # get highest probability
        maxNum = max(eng, ita, fre)

        if (maxNum == eng):
            outputs += [str(line) + ' English\n']
        elif (maxNum == ita):
            outputs += [str(line) + ' Italian\n']
        elif (maxNum == fre):
            outputs += [str(line) + ' French\n']
        else:
            outputs += ['No Result\n']
        line += 1

    # compute and output accuracy with lang.sol
    # print(outputs)
    checkSol(outputs)
