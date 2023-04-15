import nltk
import sys

def extract_clauses(text):

    sentences = nltk.sent_tokenize(text)
    clauses = []

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        clauses_tags = []
        for i, (word, tag) in enumerate(pos_tags):
            if tag in ('IN', 'DT', 'TO', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'): # get verb phrase tags
                if i > 0 and pos_tags[i-1][1] not in ('IN', 'DT', 'TO', 'CC'): # omit tags
                    clauses.append(' '.join(clauses_tags))
                    clauses_tags = []
                clauses_tags.append(word) # add to clause_tag list
            else:
                clauses_tags.append(word)
        clauses.append(' '.join(clauses_tags)) # add to clause tag list
    return clauses

text = sys.argv[1]

if len(text) > 10:
    clauses = extract_clauses(text)
    clauses = [''.join(x) for x in zip(clauses[0::2], clauses[1::2])]
    if len(clauses) > 1:
        print("That fact was a complex sentence!")
    else:
        print("That fact was a simple sentence.")
