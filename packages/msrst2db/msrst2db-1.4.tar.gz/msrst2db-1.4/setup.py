#!/usr/bin/env python
from setuptools import setup, find_packages

long_desc = """
Usage
-----

::

  rst2db <filename> [-e root_element] [-o output_file]

Only the filename to process is required. All other settings are optional.

Settings:

  -e root_element  set the root element of the resulting docbook file. If this
                   is not specified, then 'section' will be used.

  -o output_file  set the output filename to write. If this is not specified,
                  then output will be sent to stdout.
"""

setup(name='msrst2db',
      description="""
        A reStructuredText to DocBook converter using Python's docutils.""",
      version='1.4',
      install_requires=['docutils>=0.12', 'lxml>=2.3'],
      extras_require={'dev': ['check-manifest',
                              'ipdb',
                              'twine',
                              'wheel']},
      packages=find_packages(),
      entry_points={
          'console_scripts': [ 'rst2db = abstrys.cmd_rst2db:run' ],
          },
      author='Aleksei Badyaev',
      author_email='a.badyaev@mousesoft.tk',
      url='https://github.com/Aleksei-Badyaev/rst2db',
      )
