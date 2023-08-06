"""
Auto-generated setup.py file.
"""

import setuptools

setuptools.setup(
    name='litework',
    version=open('VERSION.txt').read(),
    author='Matthew Cotton',
    author_email='matt@thecottons.com',
    packages=['litework'],
    # py_modules=[],
    scripts=[
        'bin/make.py',
        'bin/work',
        'bin/workcd',
        'bin/workon',
        'bin/workadd',
        'bin/workmake',
        ],
    url='http://pypi.python.org/pypi/litework/',
    license='MIT - LICENSE.txt',
    description='Tools for rapidly preparing PyPI projects',
    long_description=open('README.rst').read(),
    install_requires=[],
)
