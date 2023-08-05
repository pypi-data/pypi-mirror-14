from codecs import open
from os import path
from setuptools import setup

__path = path.abspath(path.dirname(__file__))

with open(path.join(__path, 'README.rst'), encoding='utf-8') as f:
    readme_desc = f.read()

setup(
    name='query_collections',
    version='0.0.1.2a7',

    description='A set of classes built for easier management of Python maps and lists',
    long_description=readme_desc,
    url='https://github.com/c4wrd/query_collections',
    author='Cory Forward',
    author_email='coryf96@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='json dictionary management query selection',
    packages=['query_collections'],
    extras_require={
        'test': ['unittest'],
    }
)
