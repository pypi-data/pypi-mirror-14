# -*- coding: utf-8 -*-
"""
--------------
sphinx-navtree
--------------

Navigation tree customization for Sphinx

* Project repository: https://github.com/bintoro/sphinx-navtree
* Documentation: https://sphinx-navtree.readthedocs.org/

Copyright © 2016 Kalle Tuure. Released under the MIT License.

"""

__version__ = '0.2.0'


import os
import shutil

from docutils import nodes
from sphinx import addnodes
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.errors import SphinxError


CSS_FILENAME = 'navtree.css'
MAXDEPTH_DEFAULT = 3

use_stylesheet = False


def update_page_context(app, pagename, templatename, context, doctree):
    context[app.config.navtree_template_var] = lambda **options: get_navtree(app, pagename, **options)


def get_navtree(app, pagename, collapse=True, **kwargs):

    shift_toc = app.config.navtree_shift
    root_links = app.config.navtree_root_links
    maxdepth = app.config.navtree_maxdepth
    try:
        maxdepth.setdefault('default', kwargs.pop('maxdepth', MAXDEPTH_DEFAULT))
    except AttributeError:
        maxdepth = {'default': maxdepth}

    toctree = app.env.get_toctree_for(pagename, app.builder, collapse=False, **kwargs)

    if shift_toc:
        newtree = addnodes.compact_paragraph()
        newtree['toctree'] = True

    for top_level_node in toctree:
        if not isinstance(top_level_node, nodes.bullet_list):
            continue
        for top_level_item in top_level_node.children:
            node_count = len(top_level_item)
            if node_count != 2:
                raise NavtreeError("Expected top-level item with exactly 2 child nodes, got %d: %s"
                                   % (node_count, top_level_item.children))
            title_node = top_level_item[0][0]  # list_item > paragraph > reference
            list_node = top_level_item[1]      # list_item > bullet_list
            if not root_links:
                # Use Text node.
                title_node = title_node[0]
            app.env._toctree_prune(node     = top_level_item,
                                   depth    = 1 if shift_toc else 2,
                                   maxdepth = maxdepth.get(title_node.astext(),
                                                           maxdepth['default']),
                                   collapse = collapse)
            if shift_toc:
                caption = nodes.caption(title_node.astext(), '', title_node)
                if root_links:
                    caption['classes'].append('link')
                newtree += caption
                newtree += list_node

    if shift_toc:
        update_navtree_classes(newtree)
        toctree = newtree
    else:
        app.env._toctree_prune(toctree, 1, 0, collapse)

    return app.builder.render_partial(toctree)['fragment']


def update_navtree_classes(toctree, depth=1):
    for node in toctree.children:
        if isinstance(node, (nodes.paragraph, nodes.list_item)):
            for idx, class_ in enumerate(node['classes']):
                if class_.startswith('toctree-l'):
                    node['classes'][idx] = 'toctree-l%d' % (depth - 1)
            update_navtree_classes(node, depth)
        elif isinstance(node, nodes.bullet_list):
            update_navtree_classes(node, depth + 1)


def setup(app):
    app.add_config_value('navtree_template_var', 'toctree', '')
    app.add_config_value('navtree_maxdepth', {}, '')
    app.add_config_value('navtree_shift', False, '')
    app.add_config_value('navtree_root_links', False, '')
    app.connect('builder-inited', init)


def init(app):
    if not isinstance(app.builder, StandaloneHTMLBuilder):
        return
    app.connect('html-page-context', update_page_context)
    app.connect('build-finished', finish)
    if app.config.navtree_shift and app.config.navtree_root_links:
        globals()['use_stylesheet'] = True
        app.add_stylesheet(CSS_FILENAME)


def finish(app, exception):
    if exception:
        return
    if use_stylesheet:
        css_src = os.path.join(os.path.dirname(__file__), CSS_FILENAME)
        css_dest = os.path.join(os.path.join(app.builder.outdir, '_static'), CSS_FILENAME)
        shutil.copyfile(css_src, css_dest)


class NavtreeError(SphinxError):
    category = 'sphinx-navtree error'

