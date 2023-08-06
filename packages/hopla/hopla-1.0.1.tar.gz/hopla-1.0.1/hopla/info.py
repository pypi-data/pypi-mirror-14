#! /usr/bin/env python
##########################################################################
# Hopla - Copyright (C) AGrigis, 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Pysphinxdoc current version
version_major = 1
version_minor = 0
version_micro = 1

# Expected by setup.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(version_major, version_minor, version_micro)

# Project descriptions
DESCRIPTION = "[hopla] Easy to use pure-Python scheduler."
LONG_DESCRIPTION = """
Easy to use pure-Python scheduler.

Overview
========

With the increasing amount of data to be treated, efficient scaling strategies
are necessary. This observation made me start 'hopla' which provides:

- a scheduler that produces human readable outputs.
- a converter that enables to execute kilometer command lines
- workers that enable local or cluster executions.


Usage
=====

The proposed module has been currently developped to execute Python scripts.
Consider the following demonstration script that lists an input folder (the
latter is available in the 'hopla.demo.my_ls_script' module)::

    # System import
    import argparse
    import os

    # Parameters to keep trace
    __hopla__ = ["directory", "files"]

    def is_directory(dirarg):
        \""" Type for argparse - checks that directory exists.
        \"""
        if not os.path.isdir(dirarg):
            raise argparse.ArgumentError(
                "The directory '{0}' does not exist!".format(dirarg))
        return dirarg

    parser = argparse.ArgumentParser(description="List a directory.")
    parser.add_argument(
        "-d", "--dir", dest="dir", required=True, metavar="PATH",
        help="a valid directory to be listed.", type=is_directory)
    parser.add_argument(
        "-v", "--verbose", dest="verbose", type=int, choices=[0, 1, 2],
        default=0,
        help="increase the verbosity level: 0 silent, [1, 2] verbose.")
    args = parser.parse_args()

    directory = args.dir
    files = os.listdir(directory)
    if args.verbose > 0:
        print(files)

Note the '__hopla__' list that specifies which parameters will be dispalyed in
the scheduler execution log. This mechanism is usefull to keep trace of
important script elements (ie., the outputs). The scaled execution of this
script on two CPUs is realized using a simple call::

    from hopla.converter import hopla
    import hopla.demo as demo

    apath = os.path.abspath(os.path.dirname(__file__))
    script = os.path.join(os.path.dirname(demo.__file__),
                          "my_ls_script.py")
    status, exitcodes = hopla(
        script, hopla_iterative_kwargs=["d"], verbose=0,
        d=[apath, apath, apath], hopla_verbose=1, hopla_cpus=2)
    for job_name, exitcode in exitcodes.items():
        if exitcode > 0:
            pprint(status[job_name]["info"])

After the execution call (through the hopla function), exit codes are
inspected. The 'hopla_verbose' has been set to one, some logging information
has been displayed::

    2015-11-06 13:24:22,733 - INFO - Using 'hopla' version '1.0.0'.
    2015-11-06 13:24:22,733 - INFO - For exitcode values:
        = 0 - no error was produced.
        > 0 - the process had an error, and exited with that code.
        < 0 - the process was killed with a signal of -1 * exitcode.
    2015-11-06 13:24:22,838 - INFO - job_0.directory = /home/ag239446/git/
        hopla/hopla/test
    2015-11-06 13:24:22,839 - INFO - job_0.files = ['__pycache__', 'test.py~',
        'test.pyc', 'test.py']
    2015-11-06 13:24:22,839 - INFO - job_0.cmd = ['/home/ag239446/git/hopla/
        hopla/demo/my_ls_script.py', '-d', '/home/ag239446/git/hopla/hopla/
        test', '--verbose', '0']
    2015-11-06 13:24:22,839 - INFO - job_0.exitcode = 0
    2015-11-06 13:24:22,839 - INFO - job_1.directory = /home/ag239446/git/
        hopla/hopla/test
    2015-11-06 13:24:22,839 - INFO - job_1.files = ['__pycache__', 'test.py~',
        'test.pyc', 'test.py']
    2015-11-06 13:24:22,840 - INFO - job_1.cmd = ['/home/ag239446/git/hopla/
        hopla/demo/my_ls_script.py', '-d', '/home/ag239446/git/hopla/hopla/
        test', '--verbose', '0']
    2015-11-06 13:24:22,840 - INFO - job_1.exitcode = 0
    2015-11-06 13:24:22,842 - INFO - job_2.directory = /home/ag239446/git/
        hopla/hopla/test
    2015-11-06 13:24:22,842 - INFO - job_2.files = ['__pycache__', 'test.py~',
        'test.pyc', 'test.py']
    2015-11-06 13:24:22,842 - INFO - job_2.cmd = ['/home/ag239446/git/hopla/
        hopla/demo/my_ls_script.py', '-d', '/home/ag239446/git/hopla/hopla/
        test', '--verbose', '0']
    2015-11-06 13:24:22,842 - INFO - job_2.exitcode = 0
    2015-11-06 13:24:22,843 - INFO - Using 'hopla' version '1.0.0'.
    2015-11-06 13:24:22,843 - INFO - For exitcode values:
        = 0 - no error was produced.
        > 0 - the process had an error, and exited with that code.
        < 0 - the process was killed with a signal of -1 * exitcode.
    2015-11-06 13:24:22,951 - INFO - job_1.directory = /home/ag239446/git/
        hopla/hopla/test
    2015-11-06 13:24:22,951 - INFO - job_1.files = ['__pycache__', 'test.py~',
        'test.pyc', 'test.py']
    2015-11-06 13:24:22,952 - INFO - job_1.cmd = ['/home/ag239446/git/hopla/
        hopla/demo/my_ls_script.py', '-d', '/home/ag239446/git/hopla/hopla/
        test', '-v', '0']
    2015-11-06 13:24:22,952 - INFO - job_1.exitcode = 0
    2015-11-06 13:24:22,952 - INFO - job_0.directory = /home/ag239446/git/
        hopla/hopla/test
    2015-11-06 13:24:22,953 - INFO - job_0.files = ['__pycache__', 'test.py~',
        'test.pyc', 'test.py']
    2015-11-06 13:24:22,953 - INFO - job_0.cmd = ['/home/ag239446/git/hopla/
        hopla/demo/my_ls_script.py', '-d', '/home/ag239446/git/hopla/hopla/
        test', '-v', '0']
    2015-11-06 13:24:22,953 - INFO - job_0.exitcode = 0
    2015-11-06 13:24:22,955 - INFO - job_2.directory = /home/ag239446/git/
        hopla/hopla/test
    2015-11-06 13:24:22,955 - INFO - job_2.files = ['__pycache__', 'test.py~',
        'test.pyc', 'test.py']
    2015-11-06 13:24:22,955 - INFO - job_2.cmd = ['/home/ag239446/git/hopla/
        hopla/demo/my_ls_script.py', '-d', '/home/ag239446/git/hopla/hopla/
        test', '-v', '0']
    2015-11-06 13:24:22,955 - INFO - job_2.exitcode = 0


Perspectives
============

It will be nice to generalize some concepts (ie., accept different kind
of script).
"""

# Main setup parameters
NAME = "hopla"
AUTHOR = "Antoine Grigis"
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
URL = "https://github.com/AGrigis/hopla"
DOWNLOAD_URL = "https://github.com/AGrigis/hopla"
LICENSE = "GPL 2+"
VERSION = __version__
