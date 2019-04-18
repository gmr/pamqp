"""
Deprecating the codec subpackage

"""
import warnings

from pamqp import decode, encode

warnings.warn('Imports for decode/encode are no longer under codec',
              DeprecationWarning)
__all__ = ['decode', 'encode']
