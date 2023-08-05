from setuptools import setup, find_packages
from tox_setuptools import __version__

setup(
    name='tox-setuptools',
    version=__version__,
    packages=find_packages(),

    license='Apache 2',
    description='Tox integration with setuptools',
    url='https://github.com/2m/tox-setuptools',
)
