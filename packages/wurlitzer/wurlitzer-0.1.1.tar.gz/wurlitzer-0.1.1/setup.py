#!/usr/bin/env python
import sys

from distutils.core import setup

long_description = """
Context managers for capturing C-level output::

    from wurlitzer import pipes

    with pipes() as (stdout, stderr):
        call_c_function()
    out = stdout.read()
    err = stderr.read()
"""

version_ns = {}
with open('wurlitzer.py') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, version_ns)

setup_args = dict(
    name='wurlitzer',
    version=version_ns['__version__'],
    author="Min RK",
    author_email="benjaminrk@gmail.com",
    description="Capture C-level output in context managers",
    long_description=long_description,
    url="https://github.com/minrk/wurlitzer",
    py_modules=['wurlitzer'],
    license="MIT",
    cmdclass={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)

if 'bdist_wheel' in sys.argv:
    from wheel.bdist_wheel import bdist_wheel
    setup_args['cmdclass']['bdist_wheel'] = bdist_wheel

if __name__ == '__main__':
    setup(**setup_args)
