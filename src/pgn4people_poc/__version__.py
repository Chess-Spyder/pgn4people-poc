"""
Provides a single source of truth for the version number. Modify the string
`__version__ = '0.0.2'` to conform to the correct version number, that should
be compliant with PEP 440.

This mechanism for setting the version number also requires the following:
1) That the __init__.py file in this directory have the snippet:

    from . __version__ import __version__

2) That the setup.cfg file in the project directory include the following
snippet:

    [metadata]
    …
    version = attr: pgn4people_poc.__version__

Generally, see the answers to “Set `__version__` of module from a file when
configuring setuptools using `setup.cfg` without `setup.py`,” Stack
Overflow, May 23, 2022.
https://stackoverflow.com/questions/72357031/set-version-of-module-from-a-file-when-configuring-setuptools-using-setup
"""


__version__ = '1.1.0'