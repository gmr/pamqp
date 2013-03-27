"""pamqp specific exceptions that do not fit within the AMQP exceptions
contained in pamqp.specification

"""


class UnmarshalingException(Exception):
    """Raised when a frame is not able to be unmarshaled."""
    def __repr__(self):
        return "Could not unmarshal %s frame: %s" % (self.args[0],
                                                     self.args[1])
