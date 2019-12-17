pamqp
=====
pamqp is a low level AMQP 0-9-1 frame encoding and decoding library for Python 3
released under the BSD license.

pamqp is not a end-user client library for talking to RabbitMQ but rather is used
by client libraries for marshaling and unmarshaling AMQP frames. All methods should
have test coverage and pass in Python 3.6+.

AMQP class/method command class mappings can be found in the :py:mod:`pamqp.commands`
module while actual frame encoding and encoding should be run through the :py:mod:`pamqp.frame`
module.

Issues
------
Please report any issues to the Github repo at `https://github.com/gmr/pamqp/issues <https://github.com/gmr/pamqp/issues>`_

Source
------
pamqp source is available on Github at  `https://github.com/gmr/pamqp <https://github.com/gmr/pamqp>`_

Installation
------------
pamqp is available from the `Python Package Index <https://pypi.python.org>`_ but should generally be installed as a dependency from a client library.

pamqp module documentation
--------------------------
.. toctree::
   :maxdepth: 2

   body
   commands
   decode
   encode
   exceptions
   frame
   header
   heartbeat

Version History
---------------
See :doc:`history`

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

