from setuptools import setup
import sys

tests_require = ['mock', 'pylint', 'pep8']
if sys.version_info < (2, 7, 0):
    tests_require.append('unittest2')


setup(name='pamqp',
      version='1.1.3',
      description='RabbitMQ Focused AMQP low-level library',
      long_description="AMQP 0-9-1 Frame Encoding and Decoding Library",
      author='Gavin M. Roy',
      author_email='gavinmroy@gmail.com',
      url='http://github.com/pika/pamqp',
      packages=['pamqp', 'pamqp.codec'],
      extras_require={'codegen': ['lxml']},
      tests_require=tests_require,
      test_suite="nose.collector",
      license='BSD',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Topic :: Communications',
                   'Topic :: Internet',
                   'Topic :: Software Development :: Libraries'],
      zip_safe=True)
