# pamqp

pamqp is a low level AMQP 0-9-1 frame encoding and decoding library for Python 3.11+.

pamqp is not an end-user client library for talking to RabbitMQ but rather is
used by client libraries for marshaling and unmarshaling AMQP frames.

[![PyPI version](https://img.shields.io/pypi/v/pamqp.svg)](https://pypi.org/project/pamqp/)
[![Tests](https://github.com/gmr/pamqp/workflows/Testing/badge.svg)](https://github.com/gmr/pamqp/actions?workflow=Testing)
[![codecov](https://img.shields.io/codecov/c/github/gmr/pamqp.svg)](https://codecov.io/github/gmr/pamqp?branch=main)
[![License](https://img.shields.io/pypi/l/pamqp.svg)](https://github.com/gmr/pamqp/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/pamqp)](https://pypi.org/project/pamqp/)

## Documentation

[pamqp.readthedocs.io](https://pamqp.readthedocs.io)

## Features

- AMQP 0-9-1 frame encoding and decoding
- Auto-generated command classes from the AMQP specification
- Support for all AMQP data types including field tables and arrays
- RabbitMQ extensions (Connection.Blocked, Connection.Unblocked, etc.)
- Full type annotations with mypy and basedpyright verification
- No runtime dependencies

## Used By

- [aio-pika](https://github.com/mosquito/aio-pika)
- [aioamqp](https://github.com/Polyconseil/aioamqp)
- [aiorabbit](https://github.com/gmr/aiorabbit)
- [aiormq](https://github.com/mosquito/aiormq)
- [amqp-mock](https://github.com/tsv1/amqp-mock)
- [carehare](https://github.com/CJWorkbench/carehare)
- [rabbitpy](https://github.com/gmr/rabbitpy)

## Installation

```bash
pip install pamqp
```

## Python Versions Supported

3.11+
