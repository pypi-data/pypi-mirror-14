from setuptools import setup

setup(
    name='tox-setuptools',
    version='1.3.3',
    py_modules=['tox_setuptools'],

    entry_points={'distutils.commands': [
        'test = tox_setuptools:ToxTest'
    ]},

    license='Apache 2',
    description='Tox integration with setuptools',
    url='https://github.com/2m/tox-setuptools',
)
