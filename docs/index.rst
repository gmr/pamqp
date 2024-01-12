pamqp
=====
pamqp is a low level AMQP 0-9-1 frame encoding and decoding library for Python 3.

pamqp is not a end-user client library for talking to RabbitMQ but rather is used
by client libraries for marshaling and unmarshaling AMQP frames.

|Version| |License|

Issues
------
Please report any issues to the Github repo at `https://github.com/gmr/pamqp/issues <https://github.com/gmr/pamqp/issues>`_

Source
------
pamqp source is available on Github at  `https://github.com/gmr/pamqp <https://github.com/gmr/pamqp>`_

Installation
------------
pamqp is available from the `Python Package Index <https://pypi.python.org>`_ but should generally be installed as a dependency from a client library.

Documentation
-------------
.. toctree::
   :maxdepth: 1

   base
   body
   commands
   common
   decode
   encode
   exceptions
   frame
   header
   heartbeat
   changelog
   genindex

License
-------

Copyright (c) 2011-2024 Gavin M. Roy
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. |Version| image:: https://img.shields.io/pypi/v/pamqp.svg?
   :target: https://pypi.python.org/pypi/pamqp
   :alt: Package Version

.. |License| image:: https://img.shields.io/pypi/l/pamqp.svg?
   :target: https://github.com/gmr/pamqp/blob/master/LICENSE
   :alt: BSD
