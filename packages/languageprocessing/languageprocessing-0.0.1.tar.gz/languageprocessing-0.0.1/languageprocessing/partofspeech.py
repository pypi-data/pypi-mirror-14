from textblob import TextBlob


class PartOfSpeech:
    def __init__(self):
        self.name = 'partofspeech'

    def analyze(self, text):
        text = TextBlob(text)
        return text.tags
