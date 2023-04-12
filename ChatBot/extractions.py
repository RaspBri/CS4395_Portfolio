import spacy
# >>> python -m spacy download en_core_web_sm
import en_core_web_sm

# Load the English language model
nlp = spacy.load('en_core_web_sm')


# Define a sample input paragraph
input_paragraph = "In the 17th century, fascination in exotic plants grew among the aristocracy of France and England, with inventor and writer Sir Hugh Platt publishing Garden of Eden in 1660, which was a book about how to grow plants indoors"
# Process the input paragraph with spaCy
doc = nlp(input_paragraph)

# Initialize variables to store the identified information
who = []
what = []
where = []
when = []

# Loop through each sentence in the paragraph
for sentence in doc.sents:
    # Use spaCy's named entity recognition to identify entities
    for entity in sentence.ents:
        if entity.label_ == 'PERSON':
            who.append(entity.text)
        elif entity.label_ == 'GPE':
            where.append(entity.text)
        elif entity.label_ == 'DATE':
            when.append(entity.text)

    # Use dependency parsing to identify the action (what)
    for token in sentence:
        if token.dep_ == 'ROOT':
            what.append(token.text)
            break

# Print out the identified information
print("Who: ", who)
print("What: ", ' '.join(what))
print("Where: ", where)
print("When: ", ' '.join(when))
