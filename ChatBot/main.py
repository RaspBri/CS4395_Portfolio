# Use ChatGPT to get website links relating to the topic the user wants to discuss
# Use links for webscraping to build corpus for chatbot
"""import openai

openai.api_key = "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"
model_engine = "gpt-3.5-turbo"

# Get user input for topic to discuss
topic = "houseplants"

# Use ChatGPT to get relevant wiki links about the user's interest
response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": ("Get 20 wikipedia links that tell me about " + topic)}
      ]
)
message = response.choices[0].message.content
file = open("links.txt", "a")
file.write(message)
file.close()
#print(str(message))

                                                    # Save jokes for later
response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": ("Tell me some jokes about " + topic)}
      ]
)
"""

import re
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # Read in links to files about user's interest
    file = open("links.txt", "r")
    # print(file.read())

    # Get URLs from .txt file
    for line in file:
        URL = (re.search("(?P<url>https?://[^\s]+)", line).group("url"))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')


        for paragraph in soup.find_all('p'):
            text = ''
            text += paragraph.text
            text = re.sub(r'\[\d+\]', '', text) # remove mini reference numbers from lines
            f = open((URL.rsplit('/', 1)[-1]) + '.txt', "a")
            f.write(text)
        #print(text)


