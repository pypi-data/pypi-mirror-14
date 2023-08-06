from codecs import open
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()


setup(
    name='GIQLogging',
    version='1.0.3',

    description='Lightweight logstash_formatter logging initializer',
    long_description=long_description,

    # Get in touch with us!
    url='https://github.com/graphiq-data/GIQLogging',
    author='Jesse Adametz - Graphiq Data Engineering',
    author_email='jesse@graphiq.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Logging',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='logging logstash_formatter',

    packages=find_packages(),
    install_requires=['logstash_formatter>=0.5.14']
)
