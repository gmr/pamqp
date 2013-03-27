.. pamqp documentation master file, created by
   sphinx-quickstart on Wed Mar 27 13:26:28 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pamqp
=====
pamqp is a low level AMQP 0-9-1 frame encoding and decoding library for Python 2 & 3 released under the BSD license.

pamqp is not a end-user client library for talking to RabbitMQ but rather is used by client libraries for marshaling and unmarshaling AMQP frames. All methods should have test coverage and pass in Python 2.6, 2.7 and 3.3.

AMQP class/method command class mappings can be found in the :py:mod:`rmqid.specification` module while actual frame encoding and encoding should be run through the :py:mod:`rmqid.frame` module.

Issues
------
Please report any issues to the Github repo at `https://github.com/pika/pamqp/issues <https://github.com/pika/pamqp/issues>`_

Source
------
pamqp source is available on Github at  `https://github.com/pika/pamqp <https://github.com/pika/pamqp>`_

Installation
------------
pamqp is available from the `Python Package Index <https://pypi.python.org>`_ but should generally be installed as a dependency from a client library using setup.py.

pamqp module documentation
--------------------------
.. toctree::
   :maxdepth: 2

   body
   codec_decode
   codec_encode
   frame
   header
   heartbeat
   specification

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

