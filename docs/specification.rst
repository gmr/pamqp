pamqp.specification
===================
The :py:mod:`pamqp.specification` module is auto-generated, created by the ``tools/codegen.py`` application. It contains all of the information about the protocol that is required for a client library to communicate with RabbitMQ or another AMQP 0-9-1 broker.

The classes inside :py:mod:`pamqp.specification` allow for the automatic marshaling and unmarshaling of AMQP method frames and Basic.Properties. In addition the command classes contain information that designates if they are synchronous commands and if so, what the expected responses are. Each commands arguments are detailed in the class and are listed in the attributes property.

:py:mod:`pamqp.specification` also implements AMQP exceptions as Python exceptions so that client libraries can raise these exceptions as is appropriate without having to implement their own extensions for AMQP protocol related issues.

.. automodule:: pamqp.specification
    :members:
