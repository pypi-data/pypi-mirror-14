# -*- coding: utf-8 -*-

from docutils.core import default_description, publish_cmdline

import writer

__version__ = '0.0.1'
__author__ = 'Yoshinobu Fujimoto'
__author_email__ = 'yosinobu@iij.ad.jp'
__license__ = 'MIT'

description = ('Generates AST from standalone '
               'reStructuredText sources.  ' + default_description)


def main():
    publish_cmdline(writer=writer.ASTWriter())
