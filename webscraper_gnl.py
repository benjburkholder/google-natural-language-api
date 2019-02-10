from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.api_core.exceptions import InvalidArgument
import six

# Documentation - https://cloud.google.com/natural-language/docs/classifying-text#language-classify-content-python

# Install Python Boilerplate Module (pip install boilerplate) - used to extract HTML from webpages.


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
        print(u'{:<16}: {}'.format('string', data))


with open('urls-gnl.txt', 'r') as b:
    content = b.readlines()
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


