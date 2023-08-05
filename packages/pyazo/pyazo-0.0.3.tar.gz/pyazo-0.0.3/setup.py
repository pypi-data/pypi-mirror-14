from setuptools import setup
import os


__version__ = '0.0.3'


def read(readme):
    return open(os.path.join(os.path.dirname(__file__), readme)).read()


setup(
    name='pyazo',
    version=__version__,
    description = 'Gyazo API client',
    author='mtwtkman',
    url='https://github.com/mtwtkman/pyazo',
    install_requires=['requests']
)
