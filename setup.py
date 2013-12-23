from setuptools import setup
import sys

from pamqp import __version__

tests_require = ['mock', 'pylint', 'pep8']
if sys.version_info < (2, 7, 0):
    tests_require.append('unittest2')


setup(name='pamqp',
      version=__version__,
      description='RabbitMQ Focused AMQP low-level library',
      long_description=open('README.rst').read(),
      author='Gavin M. Roy',
      author_email='gavinmroy@gmail.com',
      url='http://pamqp.readthedocs.org',
      package_data={'': ['LICENSE', 'README.rst']},
      packages=['pamqp', 'pamqp.codec'],
      extras_require={'codegen': ['lxml']},
      tests_require=tests_require,
      test_suite="nose.collector",
      license=open('LICENSE').read(),
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Topic :: Communications',
                   'Topic :: Internet',
                   'Topic :: Software Development :: Libraries'],
      zip_safe=True)
