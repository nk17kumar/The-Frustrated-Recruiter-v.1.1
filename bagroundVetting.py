from textblob import TextBlob

class Chat:

    @staticmethod
    def getSentimentScore(text):
        blob = TextBlob(text)
        return blob.sentiment
