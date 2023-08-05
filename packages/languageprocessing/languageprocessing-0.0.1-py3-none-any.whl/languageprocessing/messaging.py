import zmq


class Messaging:
    def __init__(self,
                 incoming_address,
                 outgoing_address,
                 context=None,
                 analyzers=None):

        context = context or zmq.Context()
        self.incoming_socket = context.socket(zmq.SUB)
        self.incoming_socket.connect(incoming_address)
        self.incoming_socket.setsockopt(zmq.SUBSCRIBE, b'')

        self.outgoing_socket = context.socket(zmq.PUB)
        self.outgoing_socket.bind(outgoing_address)

        self.analyzers = analyzers


    def run(self):
        while True:
            incoming_text = self.incoming_socket.recv().decode('ascii')

            analysis_dict = {}
            for analyzer in self.analyzers:
                result = analyzer.analyze(incoming_text)
                analysis_dict[analyzer.name] = result
            # Note: need to convert everything to ascii
            # for k, v in analysis_dict.items():
                # values should be iterable, wrangle to ascii using tuple
                # comprehension
                # v = (x.encode('ascii') for x in v)

                # explicity encode the key, use tuple unpack for values
                # frame = (k.encode('ascii'), *v)
                # send data
            self.outgoing_socket.send_pyobj(analysis_dict)
