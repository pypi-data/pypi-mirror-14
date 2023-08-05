#!/usr/bin/python

"""
Sets up a universal git/PyPI work environment (also for virtualenv).

Matthew Cotton

Steps:
    - make directory
    - cd
    - make README.rst
    - link README
    - make version.txt
    - make CHANGES.txt
    - make TODO.txt
    - make LICENSE.txt
    - make MANIFEST.in
    - generate setup.py
    - make code folder (lowercase) and __init__.py
    - git init / gitignore
"""

# standard
import argparse
import datetime
import os
import re
import subprocess
import sys

########################################

REGEX_PROJECT_NAME = r"[a-zA-Z][a-zA-Z0-9_-]{0,126}"

SETUP_FILE_FORMAT = '''\
"""
Auto-generated setup.py file.
"""

import setuptools

setuptools.setup(
    name='{lowername}',
    version=open('VERSION.txt').read(),
    author='Matthew Cotton',
    author_email='matt@thecottons.com',
    packages=['{lowername}'],
    # py_modules=[],
    # scripts=[],
    url='http://pypi.python.org/pypi/{lowername}/',
    license='MIT - LICENSE.txt',
    description={short_description},
    long_description=open('README.rst').read(),
    install_requires=[],
)
'''

README_FORMAT = '''\
{long_description}

Features
========
TBD

Installation
============
TBD

Usage
=====
TDB
'''

LICENSE = '''\
The MIT License (MIT)
Copyright (c) {year} Matthew Cotton

Permission  is hereby granted, free of charge, to any person obtaining a copy of
this  software  and  associated documentation files (the "Software"), to deal in
the  Software  without  restriction,  including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the  Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The  above  copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE  SOFTWARE  IS  PROVIDED  "AS  IS",  WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR  A  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT  HOLDERS  BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN  AN  ACTION  OF  CONTRACT,  TORT  OR  OTHERWISE,  ARISING  FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

GITIGNORE = """\
venv.txt

.DS_Store

build/
dist/
*.egg-info

*.pyc
*.log
*.log.*
*.tar.gz"""

MANIFEST = """\
include setup.py
include CHANGES.txt
include LICENSE.txt
include MANIFEST.in
include README.rst
include TODO.txt
include VERSION.txt
"""

########################################
# convenience methods

def err(msg):
    """Print error and exit with code 1."""
    print "[-] {}".format(msg)
    sys.exit(1)

def log(msg):
    """Print message."""
    print "[ ] {}".format(msg)

def end(msg):
    """Print the final message and end successfully."""
    print "[+] {}".format(msg)
    sys.exit(0)

########################################
# main

def check(name, root):
    """Confirm directory is available."""
    os.chdir(root)

    # check for project
    log("Checking for directory...")
    if os.path.isdir(name):
        err("Project path '{}' already exists!".format(name))


def make(name, root):
    """Prepare project directory."""
    try:
        short_description = repr(raw_input("Short pitch: "))
        long_description = raw_input("Long description (one line): ")
    except KeyboardInterrupt:
        print
        err("Cancelling make.py...")

    os.chdir(root)

    # make project folder and 'cd'
    os.mkdir(name)
    os.chdir(name)

    # README.rst and README
    log("Making README.rst...")
    with open("README.rst", 'w') as readme:
        readme.write(README_FORMAT.format(long_description=long_description))
    # log("Linking README...")
    # os.symlink("README.rst", "README")

    # VERSION.txt and CHANGES.txt
    log("Making VERSION.txt...")
    with open("VERSION.txt", 'w') as version:
        version.write("0.0.1")
    log("Making CHANGES.txt...")

    now = datetime.datetime.now()

    with open("CHANGES.txt", 'w') as changes:
        timestamp = now.strftime("%-m-%-d-%y")
        changes.write("{}, {} -- {}".format("v0.0.1", timestamp, "Initial release."))

    # LICENSE.txt
    log("Making LICENSE.txt...")
    with open("LICENSE.txt", 'w') as license:
        year = now.strftime('%Y')
        license.write(LICENSE.format(year=year))

    # TODO.txt
    log("Making TODO.txt...")
    with open("TODO.txt", 'w') as todo:
        todo.write("- update auto-generated files")


    # MANIFEST.in
    log("Making MANIFEST.in...")
    with open("MANIFEST.in", 'w') as manifest:
        manifest.write(MANIFEST)

    # setup.py
    lowername = name.lower()
    log("Making setup.py...")
    with open("setup.py", 'w') as setup:
        setup.write(SETUP_FILE_FORMAT.format(
            lowername=lowername,
            short_description=short_description))

    # code folder and __init__.py
    log("Making code folder and __init__.py...")
    os.mkdir(lowername)
    with open(os.path.join(lowername, "__init__.py"), 'w') as _:
        pass

    ########################################
    # git

    # gitignore
    log("Making gitignore...")
    with open(".gitignore", 'w') as gitignore:
        gitignore.write(GITIGNORE)

    # git init
    log("Initializing git...")
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'add', '--all'])
    subprocess.call(['git', 'commit', '-m', "'Initial commit (auto)'"])

    end("Setup successful!")


def parse_args():
    """Get command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="project name")
    parser.add_argument("--root", type=str, default=None,
                        help="root directory of where to make the project")
    args = parser.parse_args()

    return args


def main():
    """Runs make with arguemnts."""
    args = parse_args()
    name = args.name
    root = args.root

    assert re.match(REGEX_PROJECT_NAME, name)
    if root:
        assert os.path.isdir(root)
    else:
        root = os.getcwd()

    # abs_path = os.path.join(root, name)
    log("Starting make.py...")
    check(name, root)
    make(name, root)

if __name__ == '__main__':
    main()
