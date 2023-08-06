from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    raise Exception("This package requires Python 3.5 or higher.")


PACKAGE_NAME = "aeroport"
VERSION = "0.0.2"
QUICK_DESCRIPTION = "Organize hub for data arrival / departures"
SOURCE_DIR_NAME = "src"


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=QUICK_DESCRIPTION,
    author="Dmitry Litvinenko",
    author_email="anti1869@gmail.com",
    long_description=readme(),
    url="https://github.com/anti1869/aeroport",
    package_dir={'': SOURCE_DIR_NAME},
    packages=find_packages(SOURCE_DIR_NAME, exclude=('*.tests',)),
    include_package_data=True,
    zip_safe=False,
    package_data={},
    license='Apache 2',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Development Status :: 2 - Pre-Alpha',
    ],
    install_requires=[
        "aiocron",
        "beautifulsoup4",
        "colorlog",
        "sunhead",
        "splinter",
    ],
    entry_points={
        'console_scripts': [
            'aeroport = aeroport.__main__:main',
        ],
    }
)
