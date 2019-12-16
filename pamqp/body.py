# -*- encoding: utf-8 -*-
"""
The pamqp.body module contains the Body class which is used when
unmarshaling body frames. When dealing with content frames, the message body
will be returned from the library as an instance of the body class.

"""
import typing


class ContentBody:
    """ContentBody carries the value for an AMQP message body frame"""
    def __init__(self, value: typing.Optional[bytes] = None):
        """Create a new instance of a ContentBody object"""
        self.value = value

    def __len__(self) -> int:
        """Return the length of the content body value"""
        return len(self.value) if self.value else 0

    def marshal(self) -> bytes:
        """Return the marshaled content body. This method is here for API
        compatibility, there is no special marshaling for the payload in a
        content frame.

        """
        return self.value

    def unmarshal(self, data: bytes) -> typing.NoReturn:
        """Apply the data to the object. This method is here for API
        compatibility, there is no special unmarhsaling for the payload in a
        content frame.

        """
        self.value = data
