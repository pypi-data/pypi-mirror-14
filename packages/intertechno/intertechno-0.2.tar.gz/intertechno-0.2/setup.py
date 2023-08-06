"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'intertechno', 'VERSION'), encoding='utf-8') as version_file:
    version = version_file.read().strip()

setup(
    name='intertechno',

    version=version,

    description='Library for communicating with intertechno devices.',
    long_description=long_description,

    url='https://github.com/smart-home-technology/intertechno-python',

    author='Smart-Home Technology GmbH',
    author_email='code@smart-home-technology.ch',

    license='MIT',
    platforms=['any'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Home Automation',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent'
    ],

    keywords='intertechno interface control home automation device',

    packages=['intertechno'],
    
    package_data={'intertechno': ['VERSION']},

    install_requires=[],

)
