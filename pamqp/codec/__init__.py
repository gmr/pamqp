"""
Deprecating the codec subpackage

"""
import warnings

warnings.warn('Imports for decode/encode are no longer under codec',
              DeprecationWarning)

from pamqp import decode
from pamqp import encode
