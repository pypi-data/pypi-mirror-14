"""Setuptools configuration for interfaces."""

from setuptools import setup
from setuptools import find_packages


with open('README.rst', 'r') as readmefile:

    README = readmefile.read()

setup(
    name='asyncdef.interfaces',
    version='0.1.2',
    url='https://github.com/asyncdef/interfaces',
    description='Public APIs for the core asyncdef components.',
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=README,
    license='Apache 2.0',
    packages=[
        'asyncdef.interfaces',
        'asyncdef.interfaces.engine',
    ],
    install_requires=[
        'iface',
    ],
    extras_require={
        'testing': [
            'pep257',
            'pep8',
            'pyenchant',
            'pyflakes',
            'pylint',
        ],
    },
    entry_points={
        'console_scripts': [

        ],
    },
    include_package_data=True,
    zip_safe=False,
)
