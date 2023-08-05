# -*- coding: utf-8 -*-
#
# abstrys.sphinx_ext.docbook_builder
# ------------------------------
#
# A DocBook builder for Sphinx, using rst2db's docbook writer.
#
# by Eron Hennessey

from abstrys.docutils_ext.docbook_writer import DocBookWriter
from docutils.core import publish_from_doctree
from sphinx.builders.text import TextBuilder
import os

class DocBookBuilder(TextBuilder):
    """Build DocBook documents from a Sphinx doctree"""

    name = 'docbook'

    def get_target_uri(self, docname, typ=None):
       return './%s.xml' % docname

    def prepare_writing(self, docnames):
        self.root_element = sphinx_app.config.docbook_default_root_element

    def write_doc(self, docname, doctree):
        docutils_writer = DocBookWriter(self.root_element, docname)
        docbook_contents = publish_from_doctree(doctree, writer=docutils_writer)
        output_file = open(os.path.join(self.outdir, '%s.xml' % docname), 'w+')
        output_file.write(docbook_contents)


def setup(app):
    global sphinx_app
    sphinx_app = app
    app.add_config_value('docbook_default_root_element', 'section', 'env')
    app.add_builder(DocBookBuilder)

