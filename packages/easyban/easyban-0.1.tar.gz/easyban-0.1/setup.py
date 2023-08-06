from setuptools import setup


setup(
    name = "easyban",
    packages = ["easyban"],
    version = "0.1",
    description = "IBAN checker",
    author = "Andy",
    license='MIT',
    author_email = "arnepeine@gmail.com",
    url = "https://pypi.python.org/pypi/easyban/",
    install_requires=['blockstack',],
    scripts=['bin/easyban'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Security :: Cryptography",
        "Topic :: Text Processing :: General"],
    long_description = """\
Universal character encoding detector
-------------------------------------

This version requires python-dev tools. (apt-get install python-dev).
"""
)
