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
      tests_require=['mock', 'unittest2', 'pylint', 'pep8'],
      test_suite = "nose.collector",
      license='BSD',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        ],
        zip_safe=True)
