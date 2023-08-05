try
===
|pypi| |license|

**try** is an easy-to-use cli tool to try out python packages.

|demo|

Features
--------

- Download packages from PyPI and GitHub
- Install in virtualenv using specific version of python
- Launch interactive python console (optional ipython) with already imported package

Usage
-----

.. code::

    try requests
    try requests --ipython
    try requests -v 3.5
    try requests -v /usr/bin/python3.4.1


Installation
------------

Use **pip** to install **try**:

.. code::

    pip3 install trypackage


Help
~~~~

**try** comes with an awesome CLI interface thanks to *click*.

.. code::

    Usage: try [OPTIONS] [PACKAGES]...

      Easily try out python packages.

    Options:
      -v, --version TEXT  The python version to use.
      --ipython           Use ipython instead of python.
      --help              Show this message and exit.
    ```

.. |pypi| image:: https://img.shields.io/pypi/v/trypackage.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/trypackage
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/timofurrer/try/master/LICENSE
    :alt: Package license

.. |demo| image:: https://asciinema.org/a/bd60nu08dbklh5d16lyd69fvx.png
    :target: https://asciinema.org/a/bd60nu08dbklh5d16lyd69fvx
    :alt: Demo
