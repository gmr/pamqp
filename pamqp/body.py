"""
ContentBody carries the value for an AMQP message body frame

"""


class ContentBody(object):

    name = 'ContentBody'

    def __init__(self, value=None):
        self.value = value

    def __len__(self):
        return len(self.value)

    def marshal(self):
        return self.value

    def unmarshal(self, data):
        self.value = data
