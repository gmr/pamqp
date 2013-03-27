"""AMQP Binary Data Encoding and Decoding

For copyright and licensing please refer to the file LICENSE

"""
from pamqp import PYTHON3

if PYTHON3:
    from pamqp.codec import decode3 as decode
    from pamqp.codec import encode3 as encode
else:
    from pamqp.codec import decode
    from pamqp.codec import encode
