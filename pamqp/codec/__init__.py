"""AMQP Binary Data Encoding and Decoding

For copyright and licensing please refer to the file COPYING

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-03-29'

from pamqp import PYTHON3

if PYTHON3:
    from pamqp.codec import decode3 as decode
    from pamqp.codec import encode3 as encode
else:
    from pamqp.codec import decode
    from pamqp.codec import encode
