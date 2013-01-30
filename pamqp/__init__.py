"""AMQP Specifications and Classes"""

__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-09-23'
__version__ = '1.0.1'

from pamqp.header import ProtocolHeader
from pamqp.header import ContentHeader

from pamqp import body
from pamqp import codec
from pamqp import frame
from pamqp import specification
