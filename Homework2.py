import sys
import pathlib
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
#nltk.download('wordnet')
#nltk.download('punkt')
#SENT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')
#nltk.download('averaged_perceptron_tagger')

# In PyCharm had to create configuration with "anat19.txt" parameter
# and added the interpreter option -s for the file to be read

# Lexical diversity of the tokenized text and output is formatted to 2 decimal places
# Number of unique tokens divided by the total number of tokens
# RETURN tokens
def calculate_diversity(raw_text):
    #tokenize raw text
    tokens = word_tokenize(raw_text)
    set1 = set(tokens) # get only unique tokens

    # remove stopwords and symbols
    tokens = [t for t in tokens if t.isalpha() and
              t not in stopwords.words('english')]
    lex_diversity = (len(set1) / len(tokens))
    print("\nLexical diversity: {:.0%}".format(lex_diversity))
    return (tokens)


# tokenize lower-case raw text, reduce tokens to only alpha w/o stopwords and length > 5
# lemmatize tokens into list of unique tokens and tag them, then find nouns
# RETURN lemmas and nouns
def preprocessing(tokens):
    token = [t.lower() for t in tokens if (len(t) > 5)]
    print("Preprocessed token count: ", len(token))

    # lemmatize the tokens
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in token]

    # use set to make list of unique tokens
    lemmas_unique = list(set(lemmas))

    # pos tagging to unique lemmas, print first twenty
    tagged_unique = nltk.pos_tag(sorted(lemmas_unique))
    print("\nThe first 20 unique tokens: ", (sorted(tagged_unique[:20])))

    # nouns from firstTwenty_tagged list
    nouns = [word for (word, pos) in tagged_unique if pos.startswith('N')]
    print("Number of tokens: ", len(token))
    print("Number of nouns: ", len(nouns))

    return lemmas, nouns


# Print list of preprocessed text where there are 5 tokens per line
def preprocessingResults(tokens, nouns):
    # New line every 5 words to help prevent horizontal scrolling
    print("\nList of tokens: ")
    for i in range(0, len(tokens), 5):
        print(tokens[i:i + 5])
    print("\nList of nouns:", nouns)


# Make dictionary of noun counts {noun:count of noun in tokens}
# print 50 most used words
# RETURN most used words
def create_dict(tokens, nouns):
    # make a dictionary w/ counts of word frequency
    counts = {t: tokens.count(t) for t in nouns}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True) # Descending Order
    most_used = sorted_counts[:50] # 50 most used words
    print("50 most common words: ", most_used)
    return most_used


# Check for letter within given word
def match(letter, word):
    # True / False
    if letter not in word:
        return False
    else:
        return True

def continue_game(rand_word, score, blanks, seen):
    # check for letter match
    user_input = input("Enter a letter: ")
    if (match(user_input, rand_word)):
        location = rand_word.find(user_input)
        if user_input not in seen:
            blanks[location] = user_input
            score += 1
            print("Right!", "\nScore:", score)
        else:
            print("Letter has already been used.")
    else:
        if user_input not in seen:
            score -= 1
            print("Sorry, guess again.", "\nScore:", score)

    seen.add(user_input)

    if rand_word in seen:
        print("You Win!")
    print(*blanks, sep='')
    return user_input, score, seen

def guessing_game(most_used):
    score = 5
    blanks = []
    seen = set() # set of seen letters
    rand_word = (random.sample(most_used, 1)[0][0]) # get random word from dictionary w/o count #
    print(rand_word)
    for i in rand_word: # underscore for each letter
        blanks += "_ "
    print(*blanks, sep='') # print list w/o brackets or commas
    user_input, score, seen = continue_game(rand_word, score, blanks, seen)

    while(score >= 0 and user_input != "!"):
        user_input, score, seen = continue_game(rand_word, score, blanks, seen)
    if (user_input == "!" or score <= -1):
        print("GAME OVER")

if __name__ == '__main__':
    #filename = input("Enter filename: ")
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        filepath = sys.argv[1]
        with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
            text_in = f.read()

        tokenList = calculate_diversity(text_in) # get list of tokenized words
        tokens, nouns = preprocessing(tokenList) # get preprocessed text and nouns
        preprocessingResults(tokens, nouns) # print preprocessing results
        most_used = create_dict(tokens, nouns) # get most used tokenized words

        print("Word Guessing Game")
        guessing_game(most_used)

