"""
    `try` - Awesome cli tool to try out python packages.

    This module contains the core functionality.

    :copyright: (c) by Timo Furrer
    :license: MIT, see LICENSE for details
"""

import tempfile
import contextlib
from subprocess import Popen
from collections import namedtuple


Package = namedtuple("Package", ["name", "url"])


def try_packages(packages, python_version, use_ipython=False):
    """Try a python package with a specific python version.

    The python version must already be installed on the system.

    :param str package: the name of the package to try
    :param str python_version: the python version for the interpreter
    """
    with use_import([x.name for x in packages]) as startup_script:
        if use_ipython:
            interpreter = build_ipython_interpreter_cmd(startup_script)
        else:
            interpreter = build_python_interpreter_cmd(startup_script)

        cmd = "{virtualenv} && {pip_install} && {interpreter}".format(
            virtualenv=build_virtualenv_cmd(python_version),
            pip_install=build_pip_cmd([x.url for x in packages]),
            interpreter=interpreter)
        proc = Popen(cmd, shell=True)
        return proc.wait() == 0


@contextlib.contextmanager
def use_import(packages):
    """Creates the python startup file for the interpreter.

    :param list packages: the name of the packages to import

    :returns: the path of the created file
    :rtype: str
    """

    with tempfile.NamedTemporaryFile(suffix=".py") as tmpfile:
        for package in packages:
            tmpfile.write("import {0}\n".format(package).encode("utf-8"))
        tmpfile.file.flush()
        yield tmpfile.name


def build_pip_cmd(packages):
    """Install the given packages using pip.

    :param list packages: the name of the packages
    """

    return "python -m pip install {0} > /dev/null".format(" ".join(packages))


def build_virtualenv_cmd(python_version):
    """Build command to create and source a
    python virtualenv using a specific python version.

    :param str python_version: the python version to use
    """
    return "virtualenv env_foo -p {0} > /dev/null && . env_foo/bin/activate".format(python_version)


def build_python_interpreter_cmd(startup_script):
    """Build command to launch python interpreter with
    already imported package.

    :param str startup_script: the script to launch on startup
    """
    return "PYTHONSTARTUP={0} python".format(startup_script)


def build_ipython_interpreter_cmd(startup_script):
    """Build command to launch ipython interpreter with
    already imported package.

    :param str startup_script: the script to launch on startup
    """
    return "{0} && PYTHONSTARTUP={1} ipython".format(build_pip_cmd("ipython"), startup_script)
