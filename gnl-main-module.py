"""
Importing other gnl modules is proving to be an issue for some reason, as a result, I'll just
inlcude all code in this module and connect it with user input fields to control the flow.
"""

import requests
from bs4 import BeautifulSoup
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six


print('Choose an analysis to run:')
print('')
print('Run Sentiment Analysis? (A)')
print('Run Content Classification? (B)')
print('Run Entities Analysis? (C)')
print('Run Entity Sentiment Analysis? (D)')
print('Run Syntax Analysis? (E)')
print('')

# Each analysis will correspond with a letter from the list above.
choice = input('Which Analysis to Run? ')

# Content Classification (gnl-classify.content.py)
if choice == 'B' or choice == 'b': 

    with open('gnl.txt', 'r') as gnl:
        content = gnl.read()
        #print(content)
        file = open('gnl2.txt', 'a')
        def classify_text(text):
            """Classifies content categories of the provided text."""
            client = language.LanguageServiceClient()

            if isinstance(text, six.binary_type):
                text = text.decode('utf-8')

            document = types.Document(
                content=text.encode('utf-8'),
                type=enums.Document.Type.PLAIN_TEXT)

            categories = client.classify_text(document).categories

            for category in categories:
                print(u'=' * 20)
                print(u'{:<16}: {}'.format('name', category.name))
                print(u'{:<16}: {}'.format('confidence', category.confidence))
                file.write(u'{:<16}: {}'.format('name', category.name) + '\n')
                file.write(u'{:<16}: {}'.format('confidence', category.confidence) + '\n')
                file.write('\n')
                file.close()

        classify_text(content)

if choice == 'D' or choice == 'd':
    with open('gnl.txt', 'r') as gnl:
        content2 = gnl.read()
        #print(content)
        file = open('gnl2.txt', 'a')

        # Instantiates a client
        client = language.LanguageServiceClient()

        document = types.Document(
            content=content2,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        #print('Text: {}'.format(content2))
        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
        #file.write('Text: {}'.format(content2))
        file.write('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude) + '\n')
        file.write('\n')
        file.close()
    
