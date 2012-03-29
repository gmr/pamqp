"""Methods for validating data structures returned in the various unit tests

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-03-29'

from decimal import Decimal
from time import mktime, struct_time


def validate_attribute(method, attribute, attribute_type, value='ignore'):
    """Validate that the given method object has the specified attribute of the
    specified attribute_type. If a value is passed in, validate that as well

    """
    if not hasattr(method, attribute):
        assert False, "%s missing %s attribute" % (method, attribute)

    if getattr(method, attribute) and \
       not isinstance(getattr(method, attribute), attribute_type):
        assert False, "%s.%s is not %s" % \
                      (method, attribute, attribute_type)

    if value != 'ignore' and value != getattr(method, attribute):
        assert False, "Expected a value of %r, received %r" % \
                      (value, getattr(method, attribute))


def compare_lists(source, dest, method='Unknown'):
    for position in xrange(0, len(source)):

        # Validate decimal, int, long, str, nothing special needed
        if isinstance(source[position], Decimal) or \
           isinstance(source[position], int) or \
           isinstance(source[position], long) or \
           isinstance(source[position], str):
            if source[position] != dest[position]:
                assert False, \
                "%s did not properly decode item in position %i '%r' vs '%r'" \
                % (method, position, source[position], dest[position])

        elif isinstance(source[position], float):
            if round(source[position], 2) != round(dest[position], 2):
                assert False, \
                "%s did not properly decode item in position %i '%r' vs '%r'" \
                % (method, position, source[position], dest[position])

        elif isinstance(source[position], struct_time):
            if mktime(source[position]) != mktime(dest[position]):
                assert False, \
                "%s did not properly decode item in position %i '%r' vs '%r'" \
                % (method, position, source[position], dest[position])

        elif isinstance(source[position], list):
            compare_lists(source[position], dest[position], method)

        elif isinstance(source[position], dict):
            compare_dicts(source[position], dest[position], method)

        else:
            assert False, "Unexpectationed item in position %i: %r" % \
                          (position, source[position])


def compare_dicts(source, dest, method='Unknown'):
    for key in source.keys():

        # Validate we have the key
        if key not in dest:
            assert False, "%s did not properly decode dict: %s missing: %r" % \
                          (method, key, dest)

        # Validate decimal, int, long, str, nothing special needed
        if isinstance(source[key], Decimal) or \
           isinstance(source[key], int) or \
           isinstance(source[key], long) or \
           isinstance(source[key], basestring):
            if source[key] != dest[key]:
                assert False, \
                "%s did not properly decode item %s '%r' vs '%r'" \
                % (method, key, source[key], dest[key])

        elif isinstance(source[key], float):
            if round(source[key], 2) != round(dest[key], 2):
                assert False, \
                "%s did not properly decode item %s '%r' vs '%r'" \
                % (method, key, source[key], dest[key])

        elif isinstance(source[key], struct_time):
            if mktime(source[key]) != mktime(dest[key]):
                assert False, \
                "%s did not properly decode item %s '%r' vs '%r'" \
                % (method, key, source[key], dest[key])

        elif isinstance(source[key], list):
            compare_lists(source[key], dest[key], method)

        elif isinstance(source[key], dict):
            compare_dicts(source[key], dest[key], method)

        else:
            assert False, "Unexpectationed item %s: %r" % \
                          (key, source[key])


def check_frame(frame, expectation):
    for key in expectation.keys():

        # Validate we have the key
        if not hasattr(frame, key):
            assert False, "%s did not have the expected key: %s" % \
                          (frame.name, key)

        # Validate decimal, int, long, str, nothing special needed
        if getattr(frame, key) != expectation[key]:
            assert False, "%s did not match the expectation for: %s" % \
                          (frame.name, key)
