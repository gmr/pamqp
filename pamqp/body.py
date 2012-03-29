"""AMQP Body Class Handler

@TODO

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'


class ContentBody(object):

    def __init__(self):
        self._fragments = list()
        self._size = 0

    def marshal(self):
        pass

    def demarshal(self, data):
        self._size += len(data)
        self._fragments.append(data)

    @property
    def content(self):
        return u''.join(self._fragments)

    @property
    def length(self):
        return self._size
