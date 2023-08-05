import socket


class ClientSocket(object):

    def __init__(self, message_length=1024):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_length = message_length

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send(self, message):
        byte_message = str.encode(message)
        self.socket.send(byte_message)

    def receive(self):
        data = self.socket.recv(self.message_length)
        return data.decode("utf-8")

    def close(self):
        self.socket.close()
