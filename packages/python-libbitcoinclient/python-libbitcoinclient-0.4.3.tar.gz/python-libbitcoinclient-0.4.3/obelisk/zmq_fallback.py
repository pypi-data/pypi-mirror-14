import zmq
from twisted.internet import task

# Some versions of ZMQ have the error in a different module.
try:
    zmq.error
except AttributeError:
    zmq.error = zmq.core.error


class ZmqSocket:

    context = zmq.Context(1)

    def __init__(self, cb, version, type=zmq.DEALER):
        self._cb = cb
        self._type = type
        if self._type == 'SUB':
            self._type = zmq.SUB
        self.public_key, self.secret_key = zmq.curve_keypair()

    def connect(self, address, public_key=None):
        self._socket = ZmqSocket.context.socket(self._type)
        if public_key:
            self._socket.curve_serverkey = public_key
            self._socket.curve_publickey = self.public_key
            self._socket.curve_secretkey = self.secret_key
        self._socket.connect(address)
        if self._type == zmq.SUB:
            self._socket.setsockopt(zmq.SUBSCRIBE, '')
        self.loop = task.LoopingCall(self.poll)
        self.loop.start(0.1)

    def poll(self):
        # keep polling till we have no more data
        while self.poll_once():
            pass

    def poll_once(self):
        try:
            data = self._socket.recv(flags=zmq.NOBLOCK)
        except zmq.error.ZMQError:
            return False
        more = self._socket.getsockopt(zmq.RCVMORE)
        self._cb(data, more)
        return True

    def send(self, data, more=0):
        if more:
            more = zmq.SNDMORE
        self._socket.send(data, more)

    def close(self):
        self.loop.stop()
        self._socket.close()
