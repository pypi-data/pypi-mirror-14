# coding=utf-8
from __future__ import unicode_literals
import re
import os
from sphinxfolders.nodes import FolderNode
from docutils.parsers.rst.directives import unchanged_required
from sphinx.util.compat import Directive

__author__ = 'flanker'


def regexp_check(argument):
    try:
        return re.compile(argument)
    except:
        raise ValueError


def extension_check(argument):
    if not re.match('\.[a-z0-9A-Z]+', argument):
        raise ValueError
    return argument


class FolderDirective(Directive):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 1
    final_argument_whitespace = False
    option_spec = {'class': unchanged_required,
                   'empty': unchanged_required,
                   'glob': unchanged_required,
                   'desc_ext': extension_check,
                   'regexp': regexp_check}

    def run(self):
        document = self.state.document
        env = self.state.document.settings.env
        rel_filename, dirname = env.relfn2path(self.arguments[0])
        rel_rootname, root = env.relfn2path('.')
        env.note_dependency(rel_filename)
        try:
            os.listdir(dirname)
        except (IOError, OSError):
            return [document.reporter.warning(
                'Unable to open directory %r' % dirname, line=self.lineno)]
        node = FolderNode()
        node['directory'] = dirname
        node['root'] = root
        node['options'] = self.options
        return [node]
