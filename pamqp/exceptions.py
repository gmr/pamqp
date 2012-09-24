"""
PAMQP Specific Exceptions

"""

class DemarshalingException(Exception):
    """Raised when a frame is not able to be demarshaled."""
    def __repr__(self):
        return "Could not demarshal %s frame: %s" % (self.args[0], self.args[1])
