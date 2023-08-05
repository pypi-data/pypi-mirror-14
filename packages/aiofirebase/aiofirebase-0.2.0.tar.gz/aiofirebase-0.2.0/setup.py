"""Setup script."""
from setuptools import find_packages
from setuptools import setup


setup(
    name='aiofirebase',
    version='0.2.0',
    packages=find_packages(),
    description='Asyncio Firebase client library',
    author='Billy Shambrook',
    author_email='billy.shambrook@gmail.com',
    install_requires=['aiohttp'],
    keywords=['firebase', 'asyncio', 'aiohttp'],
    url='https://github.com/billyshambrook/aiofirebase'
)
