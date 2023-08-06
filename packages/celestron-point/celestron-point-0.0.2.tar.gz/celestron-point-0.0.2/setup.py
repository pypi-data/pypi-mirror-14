import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "celestron-point",
    version = "0.0.2",
    author = "Christopher Troup",
    author_email = "minichate@gmail.com",
    description = ('Control Celestron telescopes from Python'),
    license = "BSD",
    keywords = "celestron, nexstar, telescope",
    url = "https://github.com/minichate/point",
    install_requires=[
        'pyserial',
    ],
    packages=find_packages(),
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
