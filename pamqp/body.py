# -*- encoding: utf-8 -*-
"""
The pamqp.body module contains the Body class which is used when
unmarshaling body frames. When dealing with content frames, the message body
will be returned from the library as an instance of the body class.

"""


class ContentBody(object):
    """ContentBody carries the value for an AMQP message body frame"""
    name = 'ContentBody'

    def __init__(self, value=None):
        """Create a new instance of a ContentBody object, passing in the value
        of the message body

        :param str|unicode|bytes value: The content body

        """
        self.value = value

    def __len__(self):
        """Return the length of the content body value

        :rtype: int

        """
        return len(self.value)

    def marshal(self):
        """Return the marshaled content body. This method is here for API
        compatibility, there is no special marhsaling for the payload in a
        content frame.

        :rtype: str|unicode|bytes

        """
        return self.value

    def unmarshal(self, data):
        """Apply the data to the object. This method is here for API
        compatibility, there is no special unmarhsaling for the payload in a
        content frame.

        :rtype: str|unicode|bytes

        """
        self.value = data
