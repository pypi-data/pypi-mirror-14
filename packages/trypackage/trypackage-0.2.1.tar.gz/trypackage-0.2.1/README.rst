try
===
|pypi| |license|

**try** is an easy-to-use cli tool to try out python packages.

|demo|

Features
--------

- Install specific package version from PyPI
- Install package from GitHub
- Install in virtualenv using specific version of python
- Specify alternative python package import name
- Keep try environment after interactive session
- Launch interactive python console with already imported package
- Launch editor instead of interpreter
- Launch arbitrary python shell instead of default python shell

Usage
-----

.. code:: bash

    try requests
    try requests --ipython
    try requests --shell ptipython
    try requests -p 3.5
    try requests -p /usr/bin/python3.4.1
    try requests==2.8.1
    try kennethreitz/requests --ipython
    try click-didyoumean:click_didyoumean  # if python package name is different then pip package name
    try requests --editor
    
Usage examples
--------------

**Try single python package:**

.. code:: bash

    try requests
    try flask
    
**Try multiple python packages in one session:**

.. code:: bash

    try requests flask
    
**Try specific version of a package:**

.. code:: bash

    try requests==2.8.1  # tries version 2.8.1 of requests instead of latest
    
**Try package from GitHub repository:**

.. code:: bash

    try <user>/<repo>  # syntax example
    try kennethreity/requests  # installs master branch of Kenneth's requests package from GitHub
    
**Try package but import with different name than package name:**

.. code:: bash

    try <package_name>:<import_name>  # syntax example
    try click-didyoumean:click_didyoumean  # install click-didyoumean but import click_didyoumean

**Try package with specific python version:**

.. code:: bash

    try requests --python 3.5  # use python3.5 in virtualenv
    try requests -p 2.7  # use python2.7 in virtualenv
    try requests -p ~/work/cpython/bin/python  # use python binary from specific location
    
**Try package with specific shell/repl:**

.. code:: bash

    try requests --shell python  # use python repl (default value)
    try requests --shell ipython  # use ipython
    try requests --shell ptpython  # use ptpython
    try requests --shell ptipython  # use ptipython
    try requests --shell bpython  # use bpython
    try requests --ipython  # use ipython - an alias for --shell ipython
    
**Try package writing a little script instead of opening shell:**

.. code:: bash

    try requests --editor  # opens $EDITOR or editor instead of shell


Configuration
-------------

``try`` can be configured to your preferences - like always use ``ipython`` as a shell or always use ``python3.5``.
The configuration file is located in your users application configuration directory in a file called ``config.ini``.
This location is OS dependent and as specified here: http://click.pocoo.org/5/api/#click.get_app_dir

The following ``config.ini`` file shows all available configuration options:


.. code:: ini

    [env]
    python=3.5
    shell=ipython
    keep=false
    always_use_editor=false
    tmpdir=~/.try


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
      -p, --python TEXT   The python version to use.
      --ipython           Use ipython instead of python.
      --shell TEXT        Specify the python shell to use. (This will override
                           --ipython
      -k, --keep          Keep try environment files.
      --editor            Try with editor instead of interpreter.
      --version           Show the version and exit.
      --help              Show this message and exit.

**try** was inspired by https://github.com/VictorBjelkholm/trymodule.

.. |pypi| image:: https://img.shields.io/pypi/v/trypackage.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/trypackage
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/timofurrer/try/master/LICENSE
    :alt: Package license

.. |demo| image:: https://asciinema.org/a/bd60nu08dbklh5d16lyd69fvx.png
    :target: https://asciinema.org/a/bd60nu08dbklh5d16lyd69fvx
    :alt: Demo
