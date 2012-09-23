"""
ContentBody carries the value for an AMQP message body frame

"""


class ContentBody(object):

    name = 'ContentBody'

    def __init__(self, value):
        self.value = value

    def demarshal(self, data):
        self.value = data
        return len(data)

    def marshal(self):
        return self.value
