from distutils.core import setup
from setuptools import find_packages

setup(
        name='firehawk',
        version='0.1',
        packages=[''],
        url='https://github.com/rustyrazorblade/firehawk',
        license='License :: OSI Approved :: Apache Software License',
        author='Jon Haddad',
        author_email='jon@jonhaddad.com',
        description='Alternative graph parsing language and REPL for DataStax Enterprise (DSE)',
        entry_points={
            'console_scripts': [
                'graph=firehawk.graph:main'
            ]
        },
        install_requires=["cassandra-driver>=3.1.0a2",
                          "docopt>=0.6.1",
                          "pyparsing>=2.1.0",
                          "colorama"]
)
