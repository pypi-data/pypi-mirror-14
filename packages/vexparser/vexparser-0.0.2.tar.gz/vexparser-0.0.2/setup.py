import os
from setuptools import find_packages, setup


# directory = os.path.abspath(os.path.dirname(__file__))
"""
with open(os.path.join(directory, 'README.rst')) as f:
    long_description = f.read()
"""

setup(
    name="vexparser",
    version='0.0.2',
    description='Command parsing for vexbot',
    # long_description=long_description,
    url='https://github.com/benhoff/commandparser',
    license='GPL3',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Operating System :: OS Independent'],
    keywords='command parsing intent classifier',
    author='Ben Hoff',
    author_email='beohoff@gmail.com',
    packages= find_packages(), # exclude=['docs', 'tests']
    install_requires=[
        'pluginmanager',
        'pyzmq',
        'numpy',
        'textblob',
        'nltk'
        ],

    extras_require={
        'dev': ['flake8']
        },
)
