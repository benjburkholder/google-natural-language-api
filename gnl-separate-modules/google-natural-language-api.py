# Need to set env variable via command line each session: https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually 
# Open Command Prompt - [set GOOGLE_APPLICATION_CREDENTIALS=[PATH]


# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'Sid has suffered some mental health issues lately, chiefly depression, and needed to speak to someone. He booked an appointment with a shrink in hopes that he could get his head straight and emotions in check.'
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


