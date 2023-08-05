from textblob import TextBlob


class SentimentAnalysis:
    def __init__(self):
        self.name = 'sentiment'

    def analyze(self, text):
        text = TextBlob(text)
        polarity = str(text.sentiment.polarity)
        subjectivity = str(text.sentiment.subjectivity)
        return {'polarity': polarity, 'subjectivity': subjectivity}
