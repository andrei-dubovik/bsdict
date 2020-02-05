from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'bsdict',
    version = '0.1.0',
    author = 'Andrei Dubovik',
    author_email = 'andrei@dubovik.eu',
    description = 'A python dictionary where keys could be lists, dictionaris, numpy arrays, etc.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/andrei-dubovik/bsdict',
    packages = find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.7',
    setup_requires = ['wheel'],
)
