#!/usr/bin/env python
"""Generates the pamqp/specification.py file used as a foundation for AMQP
communication.

"""
__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-03-31'

CODEGEN_DIR = '../codegen/'
CODEGEN_IGNORE_CLASSES = ['access']
CODEGEN_JSON = CODEGEN_DIR + 'amqp-rabbitmq-0.9.1.json'
CODEGEN_XML = CODEGEN_DIR + 'amqp0-9-1.xml'
CODEGEN_OUTPUT = '../pamqp/specification.py'
CODEGEN_JSON_URL = ('http://hg.rabbitmq.com'
                    '/rabbitmq-codegen/archive/default.tar.bz2')
CODEGEN_XML_URL = 'http://www.rabbitmq.com/resources/specs/amqp0-9-1.xml'

XPATH_ORDER = ['class', 'constant', 'method', 'field']
PREPEND = [CODEGEN_DIR + 'include.py']

import copy
from datetime import date
from json import load
from keyword import kwlist
from lxml import etree
from os import unlink
from os.path import exists
from tarfile import open as tarfile_open
from tempfile import NamedTemporaryFile
from textwrap import wrap
from urllib import urlopen

# Outut buffer list
output = []


def new_line(text='', indent=0):
    """Append a new line to the output buffer"""
    global output
    if text:
        text = text.rstrip()
    output.append(''.join([' ' for x in range(indent)]) + text)


def classify(text):
    """Replace the AMQP constant with a more pythonic classname"""
    parts = text.split('-')
    class_name = ''
    for part in parts:
        class_name += part.title()
    return class_name


def comment(text, indent=0, prefix='# '):
    """Append a comment to the output buffer"""
    lines = get_comments(text, indent + len(prefix), prefix)
    for line in lines:
        new_line(line)


def get_comments(text, indent=0, prefix='# '):
    """Return a list of lines for a given comment with the comment prefix"""
    indent_text = prefix.rjust(indent)
    lines = wrap(text, 79 - len(indent_text))
    comments = list()
    for line in lines:
        comments.append(indent_text + line)
    return comments


def dashify(text):
    """Replace a - with a _ for the passed in text"""
    return text.replace('-', '_')


def pep8_class_name(value):
    """Returns a class name in the proper case per PEP8"""
    output = list()
    parts = value.split('-')
    for part in parts:
        output.append(part[0:1].upper() + part[1:])
    return ''.join(output)


def get_class_definition(name, class_list):
    """Iterates through class_list trying to match the name against what was
    passed in.

    """
    for definition in class_list:
        if definition['name'] == name:
            return definition

    # We didn't find it, return none
    return None

def get_documentation(search_path):

    search = list()
    for key in XPATH_ORDER:
        if key in search_path:
            search.append('%s[@name="%s"]' % (key, search_path[key]))

    node = xml.xpath('%s/doc' % '/'.join(search))

    # Did we not find it? Look for a RabbitMQ extension
    if not node:
        node = rabbitmq.xpath('%s/doc' % '/'.join(search))


    # Look for RabbitMQ extensions of methods
    if not node and 'field' in search_path:
        node = rabbitmq.xpath('field[@name="%s"]/doc' % search_path['method'])

    # Look for RabbitMQ extensions of fields
    if not node and 'field' in search_path:
        node = rabbitmq.xpath('field[@name="%s"]/doc' % search_path['field'])

    # if we found it, strip all the whitespace
    if node:
        return ' '.join([line.strip()
                         for line in node[0].text.split('\n')]).strip()

    # Not found, return None
    return None


def get_label(search_path):
    # Look to see if documented & if so, provide the doc as a comment
    search = list()
    for key in XPATH_ORDER:
        if key in search_path:
            search.append('%s[@name="%s"]' % (key, search_path[key]))

    node = xml.xpath('%s' % '/'.join(search))

    if not node:
        node = rabbitmq.xpath('%s' % '/'.join(search))

    # Did it have a value by default?
    if node and 'label' in node[0].attrib:
        return node[0].attrib['label'][0:1].upper() + \
               node[0].attrib['label'][1:]
    elif node and node[0].text:
        return node[0].text.strip()[0:1].upper() + \
               node[0].text.strip()[1:].strip()

    # Look in domains
    if 'field' in search_path:
        node = xml.xpath('//amqp/domain[@name="%s"]' % search_path['field'])
        if node and 'label' in node[0].attrib:
            return node[0].attrib['label'][0:1].upper() + \
                   node[0].attrib['label'][1:]

    # Look for RabbitMQ extensions of fields
    if 'field' in search_path:
        node = rabbitmq.xpath('field[@name="%s"]' % search_path['field'])
        if node and 'label' in node[0].attrib:
            return node[0].attrib['label'][0:1].upper() + \
                   node[0].attrib['label'][1:]
        elif node and node[0].text:
            return node[0].text.strip()[0:1].upper() + \
                   node[0].text.strip()[1:].strip()

    print('Label couldn\'t find %r' % search_path)
    return None


def argument_name(name):
    """Returns a valid python argument name for the AMQP argument passed in

    :param str name: The argument name

    """
    output = name.replace('-', '_')
    if output in kwlist:
        output += '_'
    return output


def get_argument_type_doc(argument):

    if 'domain' in argument:
        for domain, data_type in amqp['domains']:
            if argument['domain'] == domain:
                argument['type'] = data_type
                break

    if 'type' in argument:
        if argument['type'] == 'bit':
            return 'bool'
        elif argument['type'] == 'long':
            return 'int/long'
        elif argument['type'] == 'longlong':
            return 'int/long'
        elif argument['type'] == 'longstr':
            return 'str'
        elif argument['type'] == 'octet':
            return 'int'
        elif argument['type'] == 'short':
            return 'int'
        elif argument['type'] == 'shortstr':
            return 'str'
        elif argument['type'] == 'table':
            return 'dict'
        elif argument['type'] == 'timestamp':
            return 'struct_time'
    return 'Unknown'


def get_argument_type(argument):

    if 'domain' in argument:
        for domain, data_type in amqp['domains']:
            if argument['domain'] == domain:
                argument['type'] = data_type
                break

    if 'type' in argument:
        return argument['type']

    return 'Unknown'


def new_function(function_name, arguments, indent=0):
    global output

    args = ['self']
    for argument in arguments:
        name = argument_name(argument['name'])
        if 'default-value' in argument and argument['default-value'] != '':
            if argument['default-value'] in kwlist or \
               isinstance(argument['default-value'], bool) or \
               isinstance(argument['default-value'], int):
                value = argument['default-value']
            else:
                if isinstance(argument['default-value'], basestring):
                    value = "'%s'" % str(argument['default-value'])
                else:
                    value = '%r' % argument['default-value']
        else:
            if argument['type'][-3:] == 'str':
                value = "''"
            elif argument['type'] in ['short', 'long']:
                value = 0
            else:
                value = 'None'
        if value == '{}':
            if argument['type'][-3:] == 'str':
                value = "''"
            elif argument['type'] in ['short', 'long']:
                value = 0
            else:
                value = 'None'

        args.append('%s=%s' % (name, value))

    # Get the definition line built
    definition = 'def %s(%s):' % (function_name, ', '.join(args))

    # Build the output of it with wrapping
    indent_str = ''.join([' ' for x in range(indent + len(function_name) + 5)])
    lines = wrap(''.join([' ' for x in range(indent)]) + definition, 79,
                 subsequent_indent=indent_str)

    for line in lines:
        new_line(line)


# Check to see if we have the codegen json file in this directory
if not exists(CODEGEN_JSON):

    # Retrieve the codegen archive
    print("Downloading codegen JSON file to %s." % CODEGEN_JSON)
    handle = urlopen(CODEGEN_JSON_URL)
    bzip2_tarball = handle.read()

    # Write the file out to a temp file
    tempfile = NamedTemporaryFile(delete=False)
    tempfile.write(bzip2_tarball)
    tempfile.close()

    # Extract the CODEGEN_JSON file to this directory
    tarball = tarfile_open(tempfile.name, 'r:*')
    archived_file = 'rabbitmq-codegen-default/' + CODEGEN_JSON.split('/')[-1]
    json_data = tarball.extractfile(archived_file)

    # Write out the JSON file
    with open(CODEGEN_JSON, 'w') as handle:
        handle.write(json_data.read())

    # Remove the tempfile
    unlink(tempfile.name)

# Read in the codegen JSON file
with open(CODEGEN_JSON, 'r') as handle:
    amqp = load(handle)

# Check to see if we have the codegen xml file in this directory
if not exists(CODEGEN_XML):

    # Retrieve the codegen XML definition
    print("Downloading codegen XML file.")
    handle = urlopen(CODEGEN_XML_URL)
    xml_content = handle.read()

    # Write out the XML file
    with open(CODEGEN_XML, 'w') as handle:
        handle.write(xml_content)

# Read in the codegen XML file
with open(CODEGEN_XML, 'r') as handle:
    amqp_xml = etree.parse(handle)
    xml = amqp_xml.xpath('//amqp')[0]

# Read in the codegen RabbitMQ Extension XML file
with open(CODEGEN_DIR + 'extensions.xml', 'r') as handle:
    rabbitmq_xml = etree.parse(handle)
    rabbitmq = rabbitmq_xml.xpath('//rabbitmq')[0]

# Our output list
output = list()

# Create and append our docblock
docblock = '''"""%s

Auto-generated AMQP Support Module

WARNING: DO NOT EDIT. To Generate run tools/codegen.py

"""
__since__ = '%s'

import struct

from pamqp import decode
from pamqp import encode
''' % (CODEGEN_OUTPUT.split('/')[-1], date.today().isoformat())

new_line(docblock)
new_line()

# AMQP Version Header
comment("AMQP Protocol Version")
new_line('VERSION = (%i, %i, %i)' % (amqp['major-version'],
                                     amqp['minor-version'],
                                     amqp['revision']))
new_line()

# Defaults
comment("RabbitMQ Defaults")
new_line('DEFAULT_HOST = "localhost"')
new_line('DEFAULT_PORT = %i' % amqp['port'])
new_line('DEFAULT_USER = "guest"')
new_line('DEFAULT_PASS = "guest"')
new_line('DEFAULT_VHOST = "/"')
new_line()

# Constant
comment("AMQP Constants")
for constant in amqp['constants']:
    if 'class' not in constant:
        # Look to see if documented & if so, provide the doc as a comment
        doc = get_documentation({'constant': constant['name'].lower()})
        if doc:
            comment(doc)
        new_line('%s = %i' % (dashify(constant['name']), constant['value']))
new_line()
comment('Not included in the spec XML or JSON files.')
new_line('FRAME_MAX_SIZE = 131072')
new_line()

# Data types
data_types = []
domains = []
for domain, data_type in amqp['domains']:
    if domain == data_type:
        data_types.append('              "%s",' % domain)
    else:
        doc = get_documentation({'domain': domain})
        if doc:
            comments = get_comments(doc, 18)
            for line in comments:
                domains.append(line)
        domains.append('           "%s": "%s",' % (domain, data_type))

comment("AMQP data types")
data_types[0] = data_types[0].replace('              ',
                                      'DATA_TYPES = [')
data_types[-1] = data_types[-1].replace(',', ']')
output += data_types
new_line()

comment("AMQP domains")
domains[0] = domains[0].replace('           ',
                                'DOMAINS = {')

domains[-1] = domains[-1].replace(',', '}')
output += domains
new_line()

comment("Other constants")
# Deprecation Warning
DEPRECATION_WARNING = 'This command is deprecated in AMQP %s' % \
                        ('-'.join([str(amqp['major-version']),
                                   str(amqp['minor-version']),
                                   str(amqp['revision'])]))
new_line('DEPRECATION_WARNING = \'%s\'' % DEPRECATION_WARNING)
new_line()


# Prepend the content from the files specified
for filename in PREPEND:
    with open(filename, 'r') as handle:
        content = handle.read()
        for line in content.split('\n'):
            new_line(line)

# Warnings and Exceptions
new_line()
comment("AMQP Errors")
errors = {}
for constant in amqp['constants']:
    if 'class' in constant:
        class_name = classify(constant['name'])
        if constant['class'] == 'soft-error':
            extends = 'Warning'
        elif constant['class'] == 'hard-error':
            extends = 'Exception'
        else:
            raise ValueError('Unexpected class: %s', constant['class'])
        new_line('class AMQP%s(%s):' % (class_name, extends))
        new_line('    """')
        # Look to see if documented & if so, provide the doc as a comment
        doc = get_documentation({'constant': constant['name'].lower()})
        if doc:
            comment(doc, 4, '')
        else:
            if extends == 'Warning':
                new_line('    Undocumented AMQP Soft Error')
            else:
                new_line('    Undocumented AMQP Hard Error')
        new_line()
        new_line('    """')
        new_line('    name = \'%s\'' % constant['name'])
        new_line('    value = %i' % constant['value'])
        new_line()
        new_line()
        errors[constant['value']] = class_name

# Error mapping to class
error_lines = []
for error_code in errors.keys():
    error_lines.append('          %i: AMQP%s,' % (error_code, errors[error_code]))
comment("AMQP Error code to class mapping")
error_lines[0] = error_lines[0].replace('          ', 'ERRORS = {')
error_lines[-1] = error_lines[-1].replace(',', '}')
output += error_lines

# Get the pamqp class list so we can sort it
class_list = list()
for amqp_class in amqp['classes']:
    if amqp_class['name'] not in CODEGEN_IGNORE_CLASSES:
        class_list.append(amqp_class['name'])

# Sort them alphabetically
#class_list.sort()

new_line()
comment("AMQP Classes and Methods")
new_line()

for class_name in class_list:

    indent = 4

    # Get the class from our JSON file
    definition = get_class_definition(class_name, amqp['classes'])
    new_line()
    new_line('class %s(object):' % pep8_class_name(class_name))

    doc = get_documentation({'class': class_name})
    label = get_label({'class': class_name}) or 'Undefined label'
    if doc:
        new_line('"""' + label, indent)
        new_line()
        comment(doc, indent, '')
        new_line()
        new_line('"""', indent)

    new_line('__slots__ = []', indent)
    new_line()
    comment("AMQP Class Number and Mapping Index", indent)
    new_line('frame_id = %i' % definition['id'], indent)
    new_line('index = 0x%08X' % (definition['id'] << 16), indent)
    new_line()

    # We use this later down in methods to get method xml to look for stuff
    # that is not in the JSON spec file beyond docs
    class_xml = xml.xpath('//amqp/class[@name="%s"]' % class_name)

    # Build the list of methods
    methods = list()
    for method in definition['methods']:
        new_line('class %s(Frame):' %
                 pep8_class_name(method['name']), indent)
        indent += 4

        # No Confirm in AMQP spec
        if class_xml:
            doc = get_documentation({'class': class_name,
                                     'method': method['name']})
            label = get_label({'class': class_name,
                               'method': method['name']}) or 'Undefined label'
            if doc:
                new_line('"""%s' % label, indent)
                new_line()
                comment(doc, indent, '')
                new_line()
                new_line('"""', indent)

        # Get the method's XML node
        if class_xml:
            method_xml = class_xml[0].xpath('method[@name="%s"]' %\
                                            method['name'])
        else:
            method_xml = None

        comment("AMQP Method Number and Mapping Index", indent)
        new_line('frame_id = %i' % method['id'], indent)
        index_value = definition['id'] << 16 | method['id']
        new_line('index = 0x%08X' % index_value, indent)
        new_line('name = \'%s.%s\'' % (pep8_class_name(class_name),
                                       pep8_class_name(method['name'])),
                 indent)
        # Add an attribute that signifies if it's a sync command
        new_line()
        comment("Specifies if this is a synchronous AMQP method", indent)
        new_line('synchronous = %s' % method.get('synchronous', False),
                 indent)

        # Add an attribute that signifies if it's a sync command
        if method.get('synchronous'):
            responses = list()
            if method_xml:
                for response in method_xml[0].iter('response'):

                    response_name = '\'%s.%s\'' %\
                                    (pep8_class_name(class_name),
                                     pep8_class_name(response.attrib['name']))
                    responses.append(response_name)
            if not responses:
                responses.append('\'%s.%sOk\'' %
                                 (pep8_class_name(class_name),
                                  pep8_class_name(method['name'])))
            new_line()
            comment('Valid responses to this method', indent)
            new_line('valid_responses = [%s]' % ', '.join(responses),
                     indent)
        new_line()


        arguments = list()
        type_keyword = False
        for argument in method['arguments']:
            name = argument_name(argument['name'])
            if name == 'type' and class_name == 'exchange':
                name = 'exchange_type'
                type_keyword = True
            arguments.append('\'%s\',' % name)

        if arguments:
            comment("AMQP Method Attributes", indent)
            arguments[-1] = arguments[-1].replace(',', ']')
            new_line('__slots__ = [' + arguments.pop(0), indent)
            for line in arguments:
                new_line(line, indent + 13)
            new_line()

        if method['arguments']:
            comment("Class Attribute Types", indent)
            for argument in method['arguments']:
                name = argument_name(argument['name'])
                if name == 'type' and class_name == 'exchange':
                    name = 'exchange_type'
                new_line('_%s = \'%s\'' % (name, get_argument_type(argument)),
                         indent)
            new_line()

        # Function definition
        arguments = copy.deepcopy(method['arguments'])
        for offset in range(0, len(arguments)):
            if arguments[offset]['name'] == 'type' and class_name == 'exchange':
                arguments[offset]['name'] = 'exchange_type'

        if arguments:
            new_function("__init__",  arguments, indent)
            indent += 4
            new_line('"""Initialize the %s.%s class' %
                     (pep8_class_name(class_name),
                      pep8_class_name(method['name'])),
                     indent)

            if type_keyword:
                new_line()
                new_line('Note that the AMQP type argument is referred to as '
                         '"%s_type" ' % class_name, indent)
                new_line('to not conflict with the Python type keyword.', indent)

            # List the arguments in the docblock
            new_line()
            for argument in method['arguments']:
                name = argument_name(argument['name'])

                if name == 'type' and class_name == 'exchange':
                    name = 'exchange_type'

                label = get_label({'class': class_name,
                                   'method': method['name'],
                                   'field': argument['name']})
                if label:
                    new_line(':param %s %s: %s' %
                             (get_argument_type_doc(argument), name, label),
                             indent)
                else:
                    new_line(':param %s %s:' % (get_argument_type_doc(argument),
                                                argument['name']), indent)

            # Note the deprecation warning in the docblock
            if method_xml and 'deprecated' in method_xml[0].attrib and \
               method_xml[0].attrib['deprecated']:
                deprecated = True
                new_line()
                new_line(':raises: DeprecationWarning', indent)
            else:
                deprecated = False

            new_line()
            new_line('"""', indent)

            # Create assignments from the arguments to attributes of the object
            for argument in method['arguments']:
                name = argument_name(argument['name'])

                if name == 'type' and class_name == 'exchange':
                    name = 'exchange_type'


                doc = get_label({'class': class_name,
                                 'method': method['name'],
                                 'field': argument['name']})
                if doc:
                    comment(doc, indent)

                if (isinstance(argument.get('default-value'), dict) and
                        not argument.get('default-value')):
                    new_line('self.%s = %s or dict()' % (name, name), indent)
                else:
                    new_line('self.%s = %s' % (name, name), indent)
                new_line()

            # Check if we're deprecated and warn if so
            if deprecated:
                comment(DEPRECATION_WARNING, indent)
                new_line('raise DeprecationWarning(DEPRECATION_WARNING)', indent)
                new_line()

            # End of function
            indent -= 4

        # End of class
        indent -= 4

    if 'properties' in definition and definition['properties']:
        new_line('class Properties(PropertiesBase):', indent)
        indent += 4
        comment('"""Content Properties"""', indent, '')
        new_line()

        new_line('name = \'%s.Properties\'' % pep8_class_name(class_name),
                 indent)
        new_line()

        new_line('__slots__ = [\'%s\',' %
                 argument_name(definition['properties'][0]['name']),
                 indent)
        for argument in definition['properties'][1:-1]:
            name = argument_name(argument['name'])
            if name == 'type':
                name = 'message_type'
            new_line('\'%s\',' % name, indent + 13)
        new_line('\'%s\']' % argument_name(definition['properties'][-1]['name']),
                 indent + 13)
        new_line()

        comment("Flag Values", indent)
        flag_value = 15
        new_line('flags = {\'%s\': %i,' %
                 (argument_name(definition['properties'][0]['name']),
                  1 << flag_value), indent)
        for argument in definition['properties'][1:-1]:
            name = argument_name(argument['name'])
            if name == 'type':
                name = 'message_type'
            flag_value -= 1
            new_line('\'%s\': %i,' % (name, 1 << flag_value), indent + 9),
        flag_value -= 1
        new_line('\'%s\': %i}' %
                 (argument_name(definition['properties'][-1]['name']),
                  1 << flag_value), indent + 9)
        new_line()

        comment("Class Attribute Types", indent)
        for argument in definition['properties']:
            name = argument_name(argument['name'])
            if name == 'type':
                name = 'message_type'
            new_line('_%s = \'%s\'' % (name, get_argument_type(argument)),
                     indent)
        new_line()
        new_line('frame_id = %i' % definition['id'], indent)
        new_line('index = 0x%04X' % definition['id'], indent)
        new_line()

        # Function definition
        properties = copy.deepcopy(definition['properties'])
        for offset in range(0, len(properties)):
            if properties[offset]['name'] == 'type':
                properties[offset]['name'] = 'message_type'

        new_function("__init__",  properties, indent)
        indent += 4
        new_line('"""Initialize the %s.Properties class' % \
                 pep8_class_name(class_name),
                 indent)
        new_line()
        new_line('Note that the AMQP property type is named message_type as '
                 'to ', indent)
        new_line('not conflict with the Python type keyword', indent)
        # List the arguments in the docblock
        new_line()
        for argument in definition['properties']:
            name = argument_name(argument['name'])
            if name == 'type':
                name = 'message_type'
            label = get_label({'class': class_name,
                               'field': argument['name']})
            if label:
                line = ':param %s %s: %s' % (get_argument_type_doc(argument),
                                             name, label or None)
                new_line(line.strip(), indent)

        new_line()
        new_line('"""', indent)

        # Create assignments from the arguments to attributes of the object
        for argument in definition['properties']:
            name = argument_name(argument['name'])
            if name == 'type':
                name = 'message_type'
            doc = get_label({'class': class_name,
                             'field': argument['name']})
            if doc:
                comment(doc, indent)

            new_line('self.%s = %s' % (name, name), indent)
            new_line()

        # End of function
        indent -= 4

comment("AMQP Class.Method Index Mapping")
mapping = list()
for amqp_class in amqp['classes']:
    if amqp_class['name'] not in CODEGEN_IGNORE_CLASSES:
        for method in amqp_class['methods']:
            key = amqp_class['id'] << 16 | method['id']
            mapping.append(('                 0x%08X: %s.%s,' %
                            (key,
                             pep8_class_name(amqp_class['name']),
                             pep8_class_name(method['name']))))
mapping[0] = mapping[0].replace('                 ',
                                'INDEX_MAPPING = {')
mapping[-1] = mapping[-1].replace(',', '}')
output += mapping
new_line()

# Spit out the file
output_string = '\n'.join(output)
with open(CODEGEN_OUTPUT, 'w') as handle:
    handle.write(output_string)
