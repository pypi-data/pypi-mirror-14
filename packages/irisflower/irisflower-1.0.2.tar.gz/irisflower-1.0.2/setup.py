from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='irisflower',
    version='1.0.2',
    description='Iris flower species classifier',
    long_description=long_description,
    url='https://github.com/risan/iris-flower-classifier',
    author='Risan Bagja Pradana',
    author_email='risanbagja@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='machine learning classifier',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'scipy>=0.9',
        'scikit-learn'
    ],
)
