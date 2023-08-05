#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rst2db.py
# =========
#
# A reStructuredText to DocBook conversion tool, using Python's docutils
# library.
#
# by Eron Hennessey

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import os
import sys

from abstrys.docutils_ext.docbook_writer import DocBookWriter
from docutils.core import publish_string


DESCRIPTION = 'rst2db - convert reStructuredText to DocBook'


def printerr(error_text):
    """Prints an error message to stderr."""
    sys.stderr.write("ERROR -- %s\n" % error_text)


def process_cmd_args():
    """Parse command-line options."""
    parser = ArgumentParser(description=DESCRIPTION,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('input_filename', metavar='INPUT',
                        help='Path to input ReST file.')
    parser.add_argument('-o', '--output',
                        dest='output_filename', metavar='OUTPUT',
                        help='Path to output DocBook file.')
    parser.add_argument('-t', '--template',
                        dest='template_filename', metavar='TEMPLATE',
                        help='Path to template DocBook file.')
    parser.add_argument('-e', '--element', dest='root_element',
                        default='section', metavar='ROOT',
                        help='Root element of the resulting DocBook file.')
    parser.add_argument('-l', '--lang', dest='lang',
                        help='Language code of the resulting DocBook file.')
    return parser.parse_args()


def run():
    """The main procedure."""
    program_name = os.path.basename(sys.argv[0])
    try:
        params = process_cmd_args()
        if not os.path.exists(params.input_filename):
            printerr("File doesn't exist: %s" % params.input_filename)
            sys.exit(1)
        # get the file contents first
        input_file_contents = open(params.input_filename, 'rb').read()
        docutils_writer = None
        # set up the writer
        if params.output_filename is not None:
            # If there's an output filename, use its basename as the root
            # element's ID.
            (_, filename) = os.path.split(params.output_filename)
            (doc_id, _) = os.path.splitext(filename)
            docutils_writer = DocBookWriter(params.root_element,
                                            doc_id,
                                            lang=params.lang)
        else:
            docutils_writer = DocBookWriter(params.root_element,
                                            lang=params.lang)
        # get the docbook output.
        overrides = {'input_encoding': 'utf-8',
                     'output_encoding': 'utf-8'}
        docbook_contents = publish_string(input_file_contents,
                                          writer=docutils_writer,
                                          settings_overrides=overrides)
        # if there's an output file, write to that. Otherwise, write to stdout.
        if params.output_filename is None:
            output_file = sys.stdout
        else:
            output_file = open(params.output_filename, 'w+')
    
        output_file.write(docbook_contents)
        # that's it, we're done here!
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * ' '
        sys.stderr.write(program_name + ': ' + repr(e) + '\n')
        sys.stderr.write(indent + '  for help use --help\n')
        return 1


if __name__ == "__main__":
    sys.exit(run())
