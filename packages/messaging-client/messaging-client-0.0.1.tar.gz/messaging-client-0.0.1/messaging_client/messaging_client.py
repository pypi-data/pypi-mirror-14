from messaging_client.client_socket import ClientSocket
from messaging_client.option_parser import DefaultOptionParser


class MessagingClient(object):

    def __init__(self, command_line_parser=None, max_message_length=1024):
        if command_line_parser:
            self.command_line_parser = command_line_parser
        else:
            self.command_line_parser = DefaultOptionParser()
        self.client = ClientSocket(message_length=max_message_length)

    def parse_command_line(self):
        """Parses the command line arguments.

        Returns:
            Dictionary containing all given command line
            arguments and options.
        """
        return self.command_line_parser.parse()

    def connect(self, host, port):
        """Connects to given host address and port."""
        self.client.connect(host, port)

    def close(self):
        """Closes the connection to remote host."""
        self.client.close()

    def _readFile(self, filename):
        data = []
        with open(filename, 'r') as file:
            data = file.readlines()
        return "".join(data)

    # TODO: send until all content of the file is sent, and not just what can fit.
    def send_file_message(self, filename, printMessage=False):
        """Send message inside the given file."""
        data = self._readFile(filename)
        if printMessage:
            print(data)
        self.client.send(data)

    def send_message(self, message, printMessage=False):
        """Send a given message to the remote host."""
        if printMessage:
            print(message)
        self.client.send(message)

    def receive_response(self):
        """Receive a response from the remote host.

        Returns:
            The received message as a string.
        """
        return self.client.receive()
