
import openai
import re, string, random
from textblob import TextBlob
import nltk
from nltk.corpus import sentiwordnet as swn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# >>> pip install vaderSentiment

def use_openai(mood):
    openai.api_key = "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"
    model_engine = "gpt-3.5-turbo"

    # Use ChatGPT to get relevant wiki links about the user's interest
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": ("what are some phrases someone who is {} would say".format(mood))}
          ]
    )
    message = response.choices[0].message.content
    message = re.findall(r'"([^"]*)"', message)
    print(message)
    return message


def choose_mood(number):
    if number == 1:
        mood = 'happy'
    elif number == 2:
        mood = 'mad'
    elif number == 3:
        mood = 'sad'
    elif number == 4:
        mood = 'mockery'
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

    return sentiment_dict['neg'], sentiment_dict['neu'], sentiment_dict['pos']

def mock(user_input):
    inp = list(user_input.lower())
    for x in range(len(inp)):
        if x % 2 == 0:
            inp[x] = inp[x].lower()
        else:
            inp[x] = inp[x].upper()

    inp = ''.join(inp)
    print(inp)


user_input = "you give boring facts"

vader_neg, vader_neu, vader_pos = sentiment(user_input)
# decide sentiment as positive, negative and neutral
if vader_pos >= 0.05:
    print("Positive")
    mood = 'happy'
elif vader_neg <= - 0.05:
    print("Negative")
    mood = random.randint(2, 4)
else:
    print("Neutral")
    mood = 'neutral'


mood = choose_mood()
message_list = use_openai(mood)

if mood == 'mockery':
    mock(user_input)
print(random.choice(message_list))
