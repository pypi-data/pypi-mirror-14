from threading import Thread
import zmq

from sentimentanalysis import SentimentAnalysis
from parser import Parser
from partofspeech import PartOfSpeech
from messaging import Messaging

context = zmq.Context()
text_address = 'tcp://127.0.0.1:5578'
result_address = 'tcp://127.0.0.1:5579'

outgoing_pub_socket = context.socket(zmq.PUB)
outgoing_pub_socket.bind(text_address)

result_socket = context.socket(zmq.SUB)
result_socket.setsockopt(zmq.SUBSCRIBE, b'')
result_socket.connect(result_address)


sentiment_analysis = SentimentAnalysis()
parser = Parser()
part_of_speech = PartOfSpeech()

analyzers = [sentiment_analysis, parser, part_of_speech]

messager = Messaging(text_address,
                     result_address,
                     context,
                     analyzers)

thread = Thread(target=messager.run)
thread.start()

example_text = b'This morning is easy like Sunday Morning'
outgoing_pub_socket.send(example_text)

result = result_socket.recv_pyobj()
print(result)
