import sys
import pathlib
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')
#nltk.download('punkt')
#SENT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')
#nltk.download('averaged_perceptron_tagger')

# In PyCharm had to create configuration with "anat19.txt" parameter
# and added the interpreter option -s for the file to be read

def calculate_diversity(raw_text):
    #tokenize raw text
    tokens = word_tokenize(raw_text)
    print("The number of tokens in raw text ", len(tokens)) #number of tokens in list

    set1 = set(tokens)
    print("\nThe number of unique tokens in raw text:", len(set1))

    # remove stopwords and symbols
    tokens = [t for t in tokens if t.isalpha() and
              t not in stopwords.words('english')]
    #print(set1) # set of all unique tokens
    lex_diversity = (len(set1) / len(tokens))
    print("\nLexical diversity: {:.0%}".format(lex_diversity))
    return (tokens)

def preprocessing(tokens):
    token = [t.lower() for t in tokens if (len(t) > 5)]
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in token]
    lemmas_unique = list(set(lemmas))
    print("\nThe number of unique lemmas: ", len(lemmas_unique))
    firstTwenty = sorted(lemmas_unique)[:20]
    print("\nThe first 20 unique tokens: ", firstTwenty)
    firstTwenty_tagged = nltk.pos_tag(firstTwenty)
    # nouns from firstTwenty_tagged list
    nouns = [word for (word, pos) in firstTwenty_tagged if pos.startswith('N')]

    print(len(nouns), " : ", nouns)


if __name__ == '__main__':
    #filename = input("Enter filename: ")
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        filepath = sys.argv[1]
        with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
            text_in = f.read()
        #print(text_in)

        tokenList = calculate_diversity(text_in)
        preprocessing(tokenList)
