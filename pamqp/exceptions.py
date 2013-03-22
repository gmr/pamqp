"""
PAMQP Specific Exceptions

"""

class UnmarshalingException(Exception):
    """Raised when a frame is not able to be unmarshaled."""
    def __repr__(self):
        return "Could not unmarshal %s frame: %s" % (self.args[0], self.args[1])
