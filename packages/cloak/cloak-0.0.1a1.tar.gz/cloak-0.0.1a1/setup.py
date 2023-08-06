from setuptools import setup
from cloak import __version__, __author__

setup(
    name='cloak',
    author=__author__,
    author_email="rpcope1@gmail.com",
    version=__version__,
    description="A library of container data structures",
    packages=['cloak'],
    install_requires=['ImmutablePy==0.1.0'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License'
    ]
)
