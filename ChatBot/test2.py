

# Get wikipedia h2 and set as tag name
# take subheaders as patterns along with top words from h2 paragraph sections
# Group paragraphs of header text into one section
# lemmatize user input and wiki sentence/paragraph to get most accurate fact1
# show user suggested sub topics to talk about
# when user asks about subtopic, pull from selected subtopic and give information based on sine similarity and tdif vectorization
# ask user if not coherent, if not translate through chatgpt
# then add mood side of things

import openai
import re, string, random
from textblob import TextBlob
import nltk
from nltk.corpus import sentiwordnet as swn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# >>> pip install vaderSentiment

def use_openai(topic):
    openai.api_key = "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"
    model_engine = "gpt-3.5-turbo"

    # Use ChatGPT to get relevant wiki links about the user's interest
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": ("Get 10 wikipedia links that tell me about " + topic)}
          ]
    )
    message = response.choices[0].message.content
    file = open("links.txt", "a")
    file.write(message)
    file.close()


def choose_mood():
    random_number = random.randint(1, 6)
    if random_number == 1:
        mood = 'happy'
    elif random_number == 2:
        mood = 'mad'
    elif random_number == 3:
        mood = 'sad'
    elif random_number == 4:
        mood = 'sarcastic'
    else:
        mood = 'neutral'
    return mood

def sentiment(text):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(text)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    print("Sentence Overall Rated As", end=" ")
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        print("Positive")
    elif sentiment_dict['compound'] <= - 0.05:
        print("Negative")
    else:
        print("Neutral")
    return sentiment_dict['neg'], sentiment_dict['neu'], sentiment_dict['pos']


#vader_neg, vader_neu, vader_pos = sentiment("I like this")
#print(vader_neg)
#print(vader_neu)
#print(vader_pos)

mood = choose_mood()
print(mood)
