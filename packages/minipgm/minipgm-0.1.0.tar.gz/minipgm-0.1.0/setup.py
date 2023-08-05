import minipgm
from distutils.core import setup
import setuptools

setup(
    name='minipgm',
    description='A minimalistic probabilistic programming framework.',
    version='0.1.0',
    author='Arnaud Rachez',
    author_email='arnaud.rachez@gmail.com',
    packages=['minipgm'],
    requires = ['numpy', 'scipy'],
)