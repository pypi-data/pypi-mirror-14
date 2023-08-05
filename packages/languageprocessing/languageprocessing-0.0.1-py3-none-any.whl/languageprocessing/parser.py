from textblob import TextBlob


class Parser:
    def __init__(self):
        self.name = 'parser'

    def analyze(self, text):
        text = TextBlob(text)
        return text.parse()
