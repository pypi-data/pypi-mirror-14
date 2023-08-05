from messaging_client.client_socket import ClientSocket
from messaging_client.option_parser import DefaultOptionParser


class MessagingClient(object):

    def __init__(self, command_line_parser=None, max_message_length=1024):
        if command_line_parser:
            self.command_line_parser = command_line_parser
        else:
            self.command_line_parser = DefaultOptionParser()
        self.socket = ClientSocket(message_length=max_message_length)
        self.debug = False

    def set_debug_mode(self, value):
        """Set debug to True or False."""
        self.debug = value

    def parse_command_line(self):
        """Parses the command line arguments.

        Returns:
            Dictionary containing all given command line
            arguments and options.
        """
        return self.command_line_parser.parse()

    def set_address(self, host, port):
        """Add host and port attributes"""
        self.host = host
        self.port = port

    def connect(self, host=None, port=None):
        """Connects to given host address and port."""
        host = self.host if host is None else host
        port = self.port if port is None else port
        self.socket.connect(host, port)

    def close(self):
        """Closes the connection to remote host."""
        self.socket.close()

    def _readFile(self, filename):
        data = []
        with open(filename, 'r') as file:
            data = file.readlines()
        return "".join(data)

    # TODO: send until all content of the file is sent, and not just what can fit.
    def send_file_message(self, filename):
        """Send message inside the given file."""
        data = self._readFile(filename)
        if self.debug:
            print(data)
        self.socket.send(data)

    def send_message(self, message):
        """Send a given message to the remote host."""
        if self.debug:
            print(message)
        self.socket.send(message)

    def receive_response(self):
        """Receive a response from the remote host.

        Returns:
            The received message as a string.
        """
        return self.socket.receive()
