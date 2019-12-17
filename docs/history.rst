Version History
===============

3.0.0a0 (2019-12-16)
--------------------
- Update to support Python 3.6+ only
- Remove convenience exports of `pamqp.headers.ContentHeader` and `pamqp.header.ProtocolHeader`
- Remove `pamqp.constants`
- Add typing annotations to all modules, callables, and classes
- pamqp.body.ContentBody.value now only supports `bytes`
- Changed `pamqp.decode.timestamp` to return a `datetime.datetime` instance instead of `time.struct_time`.
- Updated `pamqp.encode.support_deprecated_rabbitmq()` to allow for toggling support.
- Changed `pamqp.encode.timestamp` to only support `datetime.datetime` and `time.struct_time` values, dropping epoch (`int`) support.
- Moved `pamqp.specification.Frame` to `pamqp.frame.Frame`
- Moved `pamqp.specification.PropertiesBase` to `pamqp.frame.BasicProperties`
- Removed `pamqp.frame.BasicProperties.to_dict()` in favor of behavior allowing for `dict(pamqp.frame.BasicProperties)`
- Optimized `pamqp.heartbeat.Heartbeat` to marshal the static frame value as a predefined class attribute.
- New `pamqp.specifications` build with type annotations and support for `Connection.UpdateSecret` and `Connection.UpdateSecretOk`.
- Removed the ability to unset a `Basic.Property` by invoking `del properties[key]`
- Move base classes for frames from `pamqp.specification` to `pamqp.base`
- Removed the deprecated `pamqp.codec` sub-package

2.3.0 (2019-04-18)
------------------
- Add :py:func:`pamqp.encode.support_deprecated_rabbitmq` function to limit data types available when encoding field-tables for older RabbitMQ versions.

2.2.0 (2019-04-18)
------------------
- Change :py:meth:`pamqp.encode.timestamp` to allow for numeric/epoch timestamps (#14 - `mosquito <https://github.com/mosquito>`_)
- Change :py:meth:`pamqp.frame.frame_parts` to a public method (#15 - `mosquito <https://github.com/mosquito>`_)
- Cleanup of code to pass configured flake8 tests
- Add support for 8-bit unsigned integer values in :py:meth:`pamqp.encode.table_integer`

2.1.0 (2018-12-28)
------------------
- Change raising a DeprecationWarning exception to using warnings.warn for deprecated AMQP methods (#13 - `dzen <https://github.com/dzen>`_)

2.0.0 (2018-09-11)
------------------
- **Change Python versions supported to 2.7 and 3.4+**
- **Always decode field table keys as strings (#6)**
   - This may be a breaking change means in Python3 keys will always be type str for short strings. This includes frame
     values and field table values.
   - In Python 2.7 if a short-string (key, frame field value, etc) has UTF-8 characters in it, it will be a `unicode` object.
- Combine test coverage across all Python versions
- Fix range for signed short integer (#7)
- Fix guards for usage of unsigned short usage in `pamqp.encode` (#7)
- Fix encoding and decoding of unsigned short (#7)
- Add support for unsigned short integer and long integer in field tables  (#10)
- Address edge case of small value in long type (#8)
- Address long string encoding inconsistency (#9)
- Cleanup unicode object & conditionals in py3 (#9)
- Add `pamqp.exceptions.PAMQPException` as a base class for pamqp specific exceptions (#4)
- Fix decoding of void values in a field table or array

1.6.1 (2015-02-05)
------------------
- Fix the encoding guard for unsigned short integers to be 65535 [rabbitpy #62]

1.6.0 (2014-12-12)
------------------
- Remove UTF-8 encoding from byte_array (#2)
- Fix AMQP Field Tables / `Basic.Properties` headers behavior:
   - Field names per spec should not exceed 128 bytes
   - long-strings should not be utf-8 encoded (only short-strings *boggle*)
- Ensure that field table long strings are not coerced to UTF-8 as specified in AMQP 0-9-1
   If a string is passed in as a long string in a field table and it contains UTF-8 characters it will be UTF-8 encoded
- Move AMQP Methods in specification.py to slotted classes
- Change `Basic.Properties` to a slotted class
- Instead of class level attributes with the same name as obj attributes, prefix class attributes for data types with an underscore
- Add new class method type() for `Basic.Properties` for accessing data type
- Add new class method type() for AMQP methods for accessing data type
- Change `Basic.Properties.attributes` to `Basic.Properties.attributes()`, returning the list of slotted attributes
- Fix a typo for booleans in the method mapping for table decoding
- `Frame.__getitem__` will now raise a KeyError instead of None for an invalid attribute
- `PropertiesBase` no longer checks to see if an attribute is set for contains
- Adds new specification tests
- More efficiently handle the frame end character in Python 3

1.5.0 (2014-11-05)
------------------
- Cleanup how UTF-8 is handled in decoding strings
- Ensure that field tables (headers property, etc) can use keys with utf-8 data
- Address missing and mis-aligned AMQP-0-9-1 field table decoding with the field type indicators from the RabbitMQ protocol errata page
- Fix a encoding by type bug introduced with 1.4 having to do with bytearrays
- Be explicit about needing a class id in the ContentHeader
- Update the tests to reflect the unicode changes
- Clean up the tests

1.4.0 (2014-11-04)
------------------
- Fix a long standing bug for non-specified responses for RabbitMQ AMQP extensions
- Refactor adding bytearrays and recoding complexity
- Add bytearray support (#1 and gmr/rabbitpy#48)
- Change encode/decode type errors from ValueError to TypeError exceptions
- Remove separate codecs for Python 2 & 3
- Move codecs from `pamqp.codec.encode` and `pamqp.codec.decode` to `pamqp.encode` and `pamqp.decode`
- Deprecate pamqp.codec
- Remove weird imports from top level __init__.py, not sure what I was thinking there
- Clean up codegen a bit to make it more PYTHON3 compatible
- Update codegen/include for new codec and PYTHON2/PYTHON3 behavior
- Update documentation
- Distribution updates:
   - Let travis upload to pypi
   - Add wheel distribution
   - Update supported python versions
   - Update classifiers

1.3.1 (2014-02-14)
------------------
- Fix encoding of long-long-integers

1.3.0 (2014-01-17)
------------------
- Remove support for short strings in field tables

1.2.4 (2013-12-22)
------------------
- Add short-short-int support

1.2.3 (2013-12-22)
------------------
- Fix distribution requirements

1.2.2 (2013-12-22)
------------------
- Add decimal data type support

1.2.1 (2013-07-29)
------------------
- Fix Confirm.Select definition

1.2.0 (2013-07-08)
------------------
- Add support for Connection.Blocked, Connection.Unblocked
- Add documentation to specification.py in the codegen process

1.1.3 (2013-03-27)
------------------
- Fix exception creation

1.1.2 (2013-03-27)
------------------
- Add Confirm.Select, Confirm.SelectOk

1.1.1 (2013-03-22)
------------------
- Remove debugging print statements (eek)

1.1.0 (2013-03-21)
------------------
- Add Python 3.3 support

1.0.1 (2012-10-02)
------------------
- Address Unicode issues
- Add void support in table arrays

1.0.0 (2012-09-24)
------------------
- Initial version
