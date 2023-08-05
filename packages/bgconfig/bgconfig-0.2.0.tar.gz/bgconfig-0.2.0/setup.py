from setuptools import setup, find_packages

__version__ = '0.2.0'
__author__ = 'Jordi Deu-Pons'
__author_email__ = 'jordi.deu@upf.edu'

setup(
    name="bgconfig",
    version=__version__,
    packages=find_packages(),
    install_requires=['configobj >= 5.0.6'],
    author=__author__,
    author_email=__author_email__,
    description="Bgconfig library to manage configuration files.",
    license="Apache License 2",
    keywords="",
    url="https://bitbucket.org/bgframework/bgconfig",
    download_url="https://bitbucket.org/bgframework/bgconfig/get/"+__version__+".tar.gz",
)
