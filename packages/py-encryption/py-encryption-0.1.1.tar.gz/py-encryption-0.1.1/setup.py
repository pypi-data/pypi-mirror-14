"""Py-Encryption

See:
https://github.com/veridu/py-encryption
"""


from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py-encryption',

    version='0.1.1',

    description='Simple Encryption in Python.',
    long_description=long_description,

    url='https://github.com/veridu/py-encryption',

    author='Veridu Ltd',
    author_email='contact@veridu.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=['security', 'encryption', 'AES', 'cipher', 'cryptography', 'symmetric key cryptography', 'crypto'],

    packages=find_packages(),

)
