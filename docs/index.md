# pamqp

pamqp is a low level AMQP 0-9-1 frame encoding and decoding library for Python 3.11+.

pamqp is not an end-user client library for talking to RabbitMQ but rather is
used by client libraries for marshaling and unmarshaling AMQP frames.

[![PyPI version](https://img.shields.io/pypi/v/pamqp.svg)](https://pypi.org/project/pamqp/)
[![Tests](https://github.com/gmr/pamqp/workflows/Testing/badge.svg)](https://github.com/gmr/pamqp/actions?workflow=Testing)
[![codecov](https://img.shields.io/codecov/c/github/gmr/pamqp.svg)](https://codecov.io/github/gmr/pamqp?branch=main)

## Installation

pamqp is available from [PyPI](https://pypi.org/project/pamqp/) but should
generally be installed as a dependency from a client library.

```bash
pip install pamqp
```

## Issues

Please report any issues to the [GitHub issue tracker](https://github.com/gmr/pamqp/issues).
