"""
ContentBody carries the value for an AMQP message body frame

"""


class ContentBody(object):

    name = 'ContentBody'

    def __init__(self, value=None):
        self.value = value

    def __len__(self):
        return len(self.value)

    def demarshal(self, data):
        self.value = data

    def marshal(self):
        return self.value
