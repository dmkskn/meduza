import sys
from setuptools import setup

assert sys.version_info >= (3, 6, 0), 'meduza requires Python 3.6+'
from pathlib import Path


BASE = Path(__file__).parent

def get_long_description() -> str:
    with open(BASE / 'README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='meduza',    
    version='18.9.0',
    license='MIT',
    author='Dima Koskin',
    author_email='dmksknn@gmail.com',
    description='A simple Python module that wraps the meduza.io API.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    url="https://github.com/dmkskn/meduza",
    py_modules=['meduza'],
    keywords='meduza media wrapper russia english russian',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    )