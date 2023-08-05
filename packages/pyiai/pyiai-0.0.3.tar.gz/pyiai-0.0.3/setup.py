"""
A library for the iai robot controller.

"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pyiai',
    version='0.0.3',
    description='A library for the iai robot controller.',
    author='Boddmg',
    author_email='boddmg@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    keywords='iai robot controller',
    install_requires=[
        'mock==1.0.1',
        'pyserial'
    ],
)
