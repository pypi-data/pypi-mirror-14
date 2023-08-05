"""Veridu Python SDK

See:
https://github.com/veridu/veridu-python
"""


from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='veridu-python',

    version='0.1.3',

    description='Veridu Python SDK',
    long_description=long_description,

    url='https://github.com/veridu/veridu-python',

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

    install_requires=['six==1.10.0'],

    keywords=['veridu', 'sdk', 'user identification', 'social media', 'online services', 'single sign on'],

    packages=find_packages(),

)
