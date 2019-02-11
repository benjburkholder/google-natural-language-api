
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.api_core.exceptions import InvalidArgument
import six
import sys

# User indicates upload method
print('-' * 20)
print('Running bulk URLs? (bulk)')
print('Uploading content directly? (direct)')
print('')
decision = input('Enter upload type: ')

# Handles content entered directly into .txt file
if decision == 'direct':
    while True:
        print('-' * 20)
        print('Choose an analysis to run:')
        print('')
        print('Run Sentiment Analysis? (A)')
        print('Run Content Classification? (B)')
        print('Run Entities Analysis? (C)')
        print('Run Entity Sentiment Analysis? (D)')
        print('Run Syntax Analysis? (E)')
        print('-' * 20)
        print('')

        # Each analysis will correspond with a letter from the list above.
        choice = input('Which Analysis to Run? ')

        # Content Classification (gnl-classify.content.py)
        if choice == 'B' or choice == 'b':

            with open('gnl.txt', 'r') as gnl:
                content = gnl.read()
                file = open('gnl.csv', 'a')

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
                        print(u'{:<16}: {}'.format('name', category.name))
                        print(u'{:<16}: {}'.format(
                            'confidence', category.confidence))
                        file.write(u'{:<16}: {}'.format(
                            'name', category.name) + '\n')
                        file.write(u'{:<16}: {}'.format(
                            'confidence', category.confidence) + '\n')
                        file.write('\n')
                        file.close()


        # Sentiment Analysis (google-natural-language-api.py)
        if choice == 'A' or choice == 'a':
            with open('gnl.txt', 'r') as gnl:
                content2 = gnl.read()
                file = open('gnl.csv', 'a')

                # Instantiates a client
                client = language.LanguageServiceClient()

                document = types.Document(
                    content=content2,
                    type=enums.Document.Type.PLAIN_TEXT)

                # Detects the sentiment of the text
                sentiment = client.analyze_sentiment(
                    document=document).document_sentiment

                # print('Text: {}'.format(content2))
                print('Sentiment: {}, {}'.format(
                    sentiment.score, sentiment.magnitude))
                # file.write('Text: {}'.format(content2))
                file.write('Sentiment: {}, {}'.format(
                    sentiment.score, sentiment.magnitude) + '\n')
                file.write('\n')
                file.close()

        # Entity Sentiment (gnl-entity-sentiment.py)
        if choice == 'D' or choice == 'd':
            with open('gnl.txt', 'r') as gnl:
                content3 = gnl.read()
                file = open('gnl.csv', 'a')

                def entity_sentiment_text(text):
                    """Detects entity sentiment in the provided text."""
                    client = language.LanguageServiceClient()

                    if isinstance(text, six.binary_type):
                        text = text.decode('utf-8')

                    document = types.Document(
                        content=text.encode('utf-8'),
                        type=enums.Document.Type.PLAIN_TEXT)

                    #  Detect and send native Python encoding to receive correct word offsets.
                    encoding = enums.EncodingType.UTF32
                    if sys.maxunicode == 65535:
                        encoding = enums.EncodingType.UTF16

                    result = client.analyze_entity_sentiment(document, encoding)

                    for entity in result.entities:
                        print('Mentions: ')
                        print(u'Name: "{}"'.format(entity.name))
                        for mention in entity.mentions:
                            print(u'  Begin Offset : {}'.format(
                                mention.text.begin_offset))
                            print(u'  Content : {}'.format(mention.text.content))
                            print(u'  Magnitude : {}'.format(
                                mention.sentiment.magnitude))
                            print(u'  Sentiment : {}'.format(
                                mention.sentiment.score))
                            print(u'  Type : {}'.format(mention.type))
                            print(u'Salience: {}'.format(entity.salience))
                            print(u'Sentiment: {}\n'.format(entity.sentiment))

                            file.write(u'  Begin Offset : {}'.format(
                                mention.text.begin_offset) + '\n')
                            file.write(u'  Content : {}'.format(
                                mention.text.content) + '\n')
                            file.write(u'  Magnitude : {}'.format(
                                mention.sentiment.magnitude) + '\n')
                            file.write(u'  Sentiment : {}'.format(
                                mention.sentiment.score) + '\n')
                            file.write(u'  Type : {}'.format(mention.type) + '\n')
                            file.write(u'Salience: {}'.format(
                                entity.salience) + '\n')
                            file.write(u'Sentiment: {}\n'.format(
                                entity.sentiment) + '\n')
                            file.write('\n')
                    file.close()
                entity_sentiment_text(content3)

        # Entity Analysis (gnl-entities.py)
        if choice == 'C' or choice == 'c':
            with open('gnl.txt', 'r') as gnl:
                content4 = gnl.read()
                file = open('gnl.csv', 'a')
                client = language.LanguageServiceClient()

                if isinstance(content4, six.binary_type):
                    content4 = content4.decode('utf-8')

                # Instantiates a plain text document.
                document = types.Document(
                    content=content4,
                    type=enums.Document.Type.PLAIN_TEXT)

                # Detects entities in the document. You can also analyze HTML with:
                # Document.type == enums.Document.Type.HTML
                entities = client.analyze_entities(document).entities

                for entity in entities:
                    entity_type = enums.Entity.Type(entity.type)
                    print('=' * 20)
                    print(u'{:<16}: {}'.format('name', entity.name))
                    print(u'{:<16}: {}'.format('type', entity_type.name))
                    print(u'{:<16}: {}'.format('salience', entity.salience))
                    print(u'{:<16}: {}'.format('wikipedia_url', entity.metadata.get('wikipedia_url', '-')))
                    print(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')))

                    file.write(u'{:<16}: {}'.format('name', entity.name) + '\n')
                    file.write(u'{:<16}: {}'.format('type', entity_type.name) + '\n')
                    file.write(u'{:<16}: {}'.format('salience', entity.salience) + '\n')
                    file.write(u'{:<16}: {}'.format('wikipedia_url', entity.metadata.get('wikipedia_url', '-')) + '\n')
                    file.write(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')) + '\n')
                    file.write('\n')
                file.close()

        # Syntax Analysis (gnl-analyze-syntax.py)
        if choice == 'E' or choice == 'e':
            with open('gnl.txt', 'r') as gnl:
                content5 = gnl.read()
                file = open('gnl.csv', 'a')

                def syntax_text(text):
                    """Detects syntax in the text."""
                    client = language.LanguageServiceClient()

                    if isinstance(text, six.binary_type):
                        text = text.decode('utf-8')

                    # Instantiates a plain text document.
                    document = types.Document(
                        content=text,
                        type=enums.Document.Type.PLAIN_TEXT)

                    # Detects syntax in the document. You can also analyze HTML with:
                    #   document.type == enums.Document.Type.HTML
                    tokens = client.analyze_syntax(document).tokens

                    # part-of-speech tags from enums.PartOfSpeech.Tag
                    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

                    for token in tokens:
                        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag], token.text.content))
                        file.write(u'{}: {}'.format(pos_tag[token.part_of_speech.tag], token.text.content) + '\n')
                        file.write('\n')
                    file.close()
                syntax_text(content5)

        # This if statment handles if while loop continues or breaks based on user input
        decision = input('Run another analysis? (Y/N) ')
        if decision == 'N' or decision == 'n':
            break

# ---- Handles bulk URL check ----
if decision == 'bulk':
    while True:
        print('-' * 20)
        print('Choose an analysis to run:')
        print('')
        print('Run Sentiment Analysis? (A)')
        print('Run Content Classification? (B)')
        print('Run Entities Analysis? (C)')
        print('Run Entity Sentiment Analysis? (D)')
        print('-' * 20)
        print('')

        # Each analysis will correspond with a letter from the list above.
        choice = input('Which Analysis to Run? ')

        # Content Classification (gnl-classify.content.py)
        if choice == 'B' or choice == 'b':
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
                    print(u'{:<16}: {}'.format('url', url))
                    print(u'{:<16}: {}'.format('name', category.name))
                    print(u'{:<16}: {}'.format('confidence', category.confidence))
                    print(u'{:<16}: {}'.format('string', data) + '\n')


            with open('urls-gnl.txt', 'r') as b:
                content = b.readlines()
                content = [line.rstrip('\n') for line in content]
                for url in content:

                    try:
                        html = urlopen(url)

                    except HTTPError as e:

                        print(f'{e} ~ {url}')

                    bs = BeautifulSoup(html, 'html.parser')

                    content = bs.find_all('p')
                    try:
                        for data in content:
                            classify_text(data)
                    except InvalidArgument as e:
                        print(f'{e} ~ {url}')


        # Sentiment Analysis (google-natural-language-api.py)
        if choice == 'A' or choice == 'a':
            with open('gnl.txt', 'r') as gnl:
                content2 = gnl.read()
                file = open('gnl.csv', 'a')

                # Instantiates a client
                client = language.LanguageServiceClient()

                document = types.Document(
                    content=content2,
                    type=enums.Document.Type.PLAIN_TEXT)

                # Detects the sentiment of the text
                sentiment = client.analyze_sentiment(
                    document=document).document_sentiment

                # print('Text: {}'.format(content2))
                print('Sentiment: {}, {}'.format(
                    sentiment.score, sentiment.magnitude))
                # file.write('Text: {}'.format(content2))
                file.write('Sentiment: {}, {}'.format(
                    sentiment.score, sentiment.magnitude) + '\n')
                file.write('\n')
                file.close()

        # Entity Sentiment (gnl-entity-sentiment.py)
        if choice == 'D' or choice == 'd':
                file = open('gnl.csv', 'a')

                def entity_sentiment_text(text):
                    """Detects entity sentiment in the provided text."""
                    client = language.LanguageServiceClient()

                    if isinstance(text, six.binary_type):
                        text = text.decode('utf-8')

                    document = types.Document(
                        content=text.encode('utf-8'),
                        type=enums.Document.Type.PLAIN_TEXT)

                    #  Detect and send native Python encoding to receive correct word offsets.
                    encoding = enums.EncodingType.UTF32
                    if sys.maxunicode == 65535:
                        encoding = enums.EncodingType.UTF16

                    result = client.analyze_entity_sentiment(document, encoding)

                    for entity in result.entities:
                        print('Mentions: ')
                        print(u'URL ~ "{}'.format(url))
                        print(u'Name: "{}"'.format(entity.name))
                        for mention in entity.mentions:
                            print(u'  Begin Offset : {}'.format(
                                mention.text.begin_offset))
                            print(u'  Content : {}'.format(mention.text.content))
                            print(u'  Magnitude : {}'.format(
                                mention.sentiment.magnitude))
                            print(u'  Sentiment : {}'.format(
                                mention.sentiment.score))
                            print(u'  Type : {}'.format(mention.type))
                            print(u'Salience: {}'.format(entity.salience))
                            print(u'Sentiment: {}\n'.format(entity.sentiment))
                            
                            """
                            file.write(u'  Begin Offset : {}'.format(
                                mention.text.begin_offset) + '\n')
                            file.write(u'  Content : {}'.format(
                                mention.text.content) + '\n')
                            file.write(u'  Magnitude : {}'.format(
                                mention.sentiment.magnitude) + '\n')
                            file.write(u'  Sentiment : {}'.format(
                                mention.sentiment.score) + '\n')
                            file.write(u'  Type : {}'.format(mention.type) + '\n')
                            file.write(u'Salience: {}'.format(
                                entity.salience) + '\n')
                            file.write(u'Sentiment: {}\n'.format(
                                entity.sentiment) + '\n')
                            file.write('\n')
                    file.close()
                            """
                with open('urls-gnl.txt', 'r') as b:
                    content = b.readlines()
                    content = [line.rstrip('\n') for line in content]
                    for url in content:

                        try:
                            html = urlopen(url)

                        except HTTPError as e:

                            print(f'{e} ~ {url}')

                        bs = BeautifulSoup(html, 'html.parser')

                        content = bs.find_all('p')
                        try:
                            for data in content:
                                entity_sentiment_text(data)
                        except InvalidArgument as e:
                            print(f'{e} ~ {url}')

        # Entity Analysis (gnl-entities.py)
        if choice == 'C' or choice == 'c':
            with open('urls-gnl.txt', 'r') as b:
                    content = b.readlines()
                    content = [line.rstrip('\n') for line in content]
                    for url in content:

                        try:
                            html = urlopen(url)

                        except HTTPError as e:

                            print(f'{e} ~ {url}')

                        bs = BeautifulSoup(html, 'html.parser')

                        content = bs.find_all('p')
                        content = str(content)
                        
                        file = open('gnl.csv', 'a')
                        client = language.LanguageServiceClient()

                        if isinstance(content, six.binary_type):
                            content = content.decode('utf-8')

                        # Instantiates a plain text document.
                        document = types.Document(
                            content=content,
                            type=enums.Document.Type.PLAIN_TEXT)

                        # Detects entities in the document. You can also analyze HTML with:
                        # Document.type == enums.Document.Type.HTML
                        entities = client.analyze_entities(document).entities

                        for entity in entities:
                            entity_type = enums.Entity.Type(entity.type)
                            print('=' * 20)
                            print(u'{:<16}~ {}'.format('url', url))
                            print(u'{:<16}: {}'.format('name', entity.name))
                            print(u'{:<16}: {}'.format('type', entity_type.name))
                            print(u'{:<16}: {}'.format('salience', entity.salience))
                            print(u'{:<16}: {}'.format('wikipedia_url', entity.metadata.get('wikipedia_url', '-')))
                            print(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')))

                            """
                            file.write(u'{:<16}: {}'.format('name', entity.name) + '\n')
                            file.write(u'{:<16}: {}'.format('type', entity_type.name) + '\n')
                            file.write(u'{:<16}: {}'.format('salience', entity.salience) + '\n')
                            file.write(u'{:<16}: {}'.format('wikipedia_url', entity.metadata.get('wikipedia_url', '-')) + '\n')
                            file.write(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-')) + '\n')
                            ile.write('\n')
                        file.close()
                            """

        # This if statment handles if while loop continues or breaks based on user input
        decision = input('Run another analysis? (Y/N) ')
        if decision == 'N' or decision == 'n':
            break
