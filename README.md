# CS4395_Portfolio

## Table of Contents
★ [Skills Gained](#skills-gained) <br>
★ [Course Reflection](#course-reflection) <br>
★ [Portfolio Setup](#portfolio-setup) <br>
★ [Text Processing 1](#text-processing-1) <br>
★ [Word Guessing Game](#word-guessing-game) <br>
★ [WordNet](#wordnet) <br>
★ [N Gram Language Model](#n-gram-language-model) <br>
★ [Web Crawler](#web-crawler) <br>
★ [Parsing Sentences](#parsing-sentences) <br>
★ [Text Classification 1](#text-classification-1) <br>
★ [ACL Paper Summary](#acl-paper-summary) <br>
★ [ChatBot](#chatbot) <br>
★ [Text Classification 2](#text-classification-2) <br>



## Skills Gained:
* Devleoped text representation techniques
* Gained insight on statistical analysis aproaches
* Learned how to create machine learning models for NLP training
* Expanded creative problem solving abilities

## Course Reflection
Before I took Human Language Technologies I knew vary little about natural language processing. After taking this course I have learned about speech processing and information retrieval/extraction. I for sure have developed an interest in the field of NLP now that I have taken this class and would like to explore more the field, possibly within my own career path or just as a side interest. To keep up with the field I think the best way would be to make and maintain connections with people currently in this space already so that I can see first hand what someone in this field is doing with NLP. My heart is in cybersecurity, so if there is a way to incorporate cyber and NLP I could see myself exploring that side of computer science in the future.

---

## Portfolio Setup 
This assignment is about setting up my Github portfolio and opening thoughts about natural language processing.
You can view my first assignment as a PDF [here](Overview_of_NLP.pdf).

---

## Text Processing 1
Check out Assignment 1 [here](Homework1.py)! Be sure to download Assignment 1's necessary [data.csv](Data_Files/data.csv) file.
#### Objectives
* Code regular expressions, I/O, and pickling
* Write a simple class in Python
* Gain experience coding in Python
#### Summary
This assignment reads in a file and processes the text into a standardized format in order for it to be more legible. Within the program an object class named Person is created which saves the attributes of each employee that is derived from the read file. After the text is processed and saved as an object, all Person objects are stored into a dictionary then displayed for the user. If incorrect information is given, the program will prompt the user for a correction before displaying the final results.
#### Getting Started
1. Open Homework.py in PyCharm.
2. Add a run/debug configuration. Set script path to the file location of this homeworks .py file. 
3. Click Run Button.
4. You will be prompted by the message below to enter "data.csv data" and click enter.
> Enter your filename as a system argument:
5. Start up complete. Program should run as expected.
#### Strengths/Weaknesses of Python for Text Processing
* Some strengths are that Python is pretty easy to pick up and learn. Python has simple and forgiving syntax. And with it being so easy to learn alongside how powerful it is makes it quite competitive for text processing compared to other languges. Another pro is that Python can also be used to write Object Oriented programs which, depending on the project, can make a program more efficient. 
* Some weaknesses would be that it seems to use a lot of memory. My reasoning for this comes from my experience pickling the file in this assignment. It seemed that pickling the file was only necessary because of the excess memory Python took on. Another downside is that Python is prone to runtime errors. That side of things became very apartent to me during my progress on the project.
#### Takeaways

During this assignment I was able to brush up on my very rusty Python knowledge and feel more comfortable with the language again. In the middle of the assignment I learned how to go from a list to an object. That was the most challenging part of the assignment for me. I also learned how to test for regular expressions in Python. That was something I had never tried before.

---
## Word Guessing Game
Check out Assignment 2 [here](Homework2.py)! Be sure to download Assignment 2's necessary [anat19.txt](Data_Files/anat19.txt) file.
#### Objectives
* Use Python and NLTK features to explore a text file and create a word guessing game
* Calculate lexical diversity of tokenized input
* Perform part of speech tagging on unique lemmas
* Make dictionary of nouns found in token list
* Create guessing game from 50 most common words list
---
## WordNet
Check out Assignment 3 [here](WordNet.ipynb)! No extra data files needed.
#### Objectives
* Demonstrate basic skills using WordNet and SentiWordNet
* Learn to identify collocations
---
## N Gram Language Model
Check out the Assignment 4 narrative [here](N_Gram/NGram_Narrative.pdf)! The code needed to run the project can be found below! 
#### Objectives
* Gain experience creating ngrams from text
* Build a language model from ngrams
* Reflect on the utility of ngram language models

[Needed files for model building](Data_Files/N_Gram_Files)
#### [Program 1](N_Gram/program1.py): Build separate language models for 3 languages with NLTK
#### [Program 2](N_Gram/program2.py): Calculate the probability for each language and output the accuracy
---
## Web Crawler
Check out Assignment 5 code [here](homework6.py) and the writeup report [here](Data_Files/WebCrawlerFullReport.pdf).
#### Objectives
* Understand the importance of corpora in NLP tasks, basic HTML, & how web sites work
* Be able to do web scraping with Beautiful Soup or other APIs
* Create a web crawler that results in a knowledge base
---
## Parsing Sentences
Check out Assignment 6 [here](HW-HLT.pdf) and the Stanford reference documentation [here](Data_Files/StanfordDependenciesManual.pdf) along with a [GitHub](https://gist.github.com/nlothian/9240750) page with parts of speech labels.
#### Objectives
* Understand concepts related to sentence syntax
* Understand the 3 types of sentence parses: PSG, dependency, and SRL
* Be able to use syntax parsers
---
## Text Classification 1
Check out Assignment 7 [here](TextClassification.ipynb) and the write up report [here](Data_Files/TextClassification.pdf).
#### Objectives
* Gain experience with sklearn using text data & text classification
* Use Naïve Bayes, Logistic Regression, and Neural Networks
---
## ACL Paper Summary
Check out Assignment 8 [here](NLPBasedDoctorRecommendations.pdf) and the reference ACL Paper [here](Data_Files/ACLPAPER.pdf).

---
## Chatbot
Checkout Assignment 9 code [here](ChatBot) and the writeup [here](ChatBot/ChatBot_WriteUp.pdf).
#### Objectives/Requirements
* Create a chatbot using NLP techniques learned in class 
* The chatbot can carry on a limited conversation in a particular domain using a knowledge base 
* Maintain user model for each user
* Personalize interactions with user
---
## Text Classification 2
Check out Assignment 10 [here](TextClassification2.ipynb) and the writeup [here](textclassification2.pdf).
#### Objectives
* Gain experience with Keras, text classification, deep learning model variations, and embeddings
* Use architectures such as RNN & CNN
* Experiment with different embedding approaches
