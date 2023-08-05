from codecs import open

from setuptools import setup, find_packages

from impediments import __version__, __author__, __email__, __license__

setup(
    name="gddkia-impediments-on-roads",
    version=__version__,
    author=__author__,
    author_email=__email__,
    url='https://github.com/tomi77/python-gddkia-impediments-on-roads',
    description='Impediments on roads provided by GDDKiA',
    long_description=open("README.rst").read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    license=__license__,
    packages=find_packages(exclude=['tests']),
    install_requires=['six']
)
