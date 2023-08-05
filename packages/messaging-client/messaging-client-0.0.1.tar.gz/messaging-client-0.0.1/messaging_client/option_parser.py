from optparse import OptionParser


class DefaultOptionParser(object):

    def __init__(self):
        self.parser = OptionParser(usage="usage: %prog [options] filename",
                                   version="%prog 1.0")
        self.parser.add_option("-f", "--file",
                               dest="filename",
                               help="File containing the message to be sent")
        self.parser.add_option("-r", "--host",
                               dest="host",
                               help="Address of remote host (default is localhost).")
        self.parser.add_option("-p", "--port",
                               type="int",
                               dest="port",
                               help="Port of the application to send a message (default: 8700")

    def parse(self):
        """Parse command line arguments and options.

        Returns:
            Dictionary containing all given command line arguments and options.
        """
        values = {}
        (options, args) = self.parser.parse_args()
        if len(args) == 1:
            self.filename = args[0]
            values['file'] = self.filename
        elif options.filename is not None:
            self.filename = options.filename
            values['file'] = self.filename
        elif options.filename is None and len(args) < 1:
            self.parser.error("No filename given!")

        if options.host is not None:
            self.host = options.host
            values['host'] = self.host
        if options.port is not None:
            self.port = options.port
            values['port'] = self.port

        self.args = args
        values['args'] = args
        self.options = options
        values['options'] = options
        return values
