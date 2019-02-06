# Documentation - https://cloud.google.com/natural-language/docs/classifying-text#language-classify-content-python

# Install Python Boilerplate Module (pip install boilerplate) - used to extract HTML from webpages.

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six

text = 'Sid has suffered some mental health issues lately, chiefly depression, and needed to speak to someone. He booked an appointment with a shrink in hopes that he could get his head straight and emotions in check.'

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



classify_text(text)