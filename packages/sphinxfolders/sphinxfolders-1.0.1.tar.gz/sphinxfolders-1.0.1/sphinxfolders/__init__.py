# coding=utf-8
"""Register all components of this extension"""

from nodes import FolderNode
from sphinxfolders.directives import FolderDirective
from visitors import visit_folder_node, depart_folder_node

__version__ = '1.0.1'


def setup(app):
    # app.add_config_value('todo_include_todos', False, False)

    # app.add_node(todolist)
    app.add_node(FolderNode, html=(visit_folder_node, depart_folder_node))
    app.add_directive('folder', FolderDirective)

#    app.add_directive('todolist', TodolistDirective)
#    app.connect('doctree-resolved', process_folder_nodes)
#    app.connect('env-purge-doc', purge_folders)
