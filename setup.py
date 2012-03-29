from setuptools import setup

setup(name='pamqp',
      version='1.0.0',
      description='RabbitMQ Focused AMQP low-level library',
      long_description="AMQP Frame Encoding and Decoding Library",
      author='Gavin M. Roy',
      author_email='gavinmroy@gmail.com',
      url='http://github.com/pika/pamqp',
      packages=['pamqp', 'pamqp.codec'],
      extras_require={'codegen': ['lxml']},
      setup_requires=['nosexcover', 'mock', 'unittest2', 'pylint', 'pep8'],
      test_suite = "nose.collector",
      license='MPL v1.1 and GPL v2.0 or newer',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        ],
        zip_safe=True)
