import setuptools

from pamqp import __version__

setuptools.setup(
    name='pamqp',
    version=__version__,
    description='RabbitMQ Focused AMQP low-level library',
    long_description=open('README.rst').read(),
    author='Gavin M. Roy',
    author_email='gavinmroy@gmail.com',
    url='http://pamqp.readthedocs.org',
    package_data={'': ['LICENSE', 'README.rst']},
    packages=['pamqp', 'pamqp.codec'],
    extras_require={'codegen': ['lxml']},
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True)
