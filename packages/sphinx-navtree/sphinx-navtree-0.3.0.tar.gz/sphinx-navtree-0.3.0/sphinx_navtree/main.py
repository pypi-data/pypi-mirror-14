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

__version__ = '0.3.0'


import os
import shutil

from docutils import nodes
from sphinx import addnodes
from sphinx.builders.html import StandaloneHTMLBuilder, SerializingHTMLBuilder
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
    navtree = addnodes.compact_paragraph()
    navtree['toctree'] = True

    for bullet_list, caption in iter_toctree(toctree):
        process_toctree_list(navtree, bullet_list, caption, app,
                             collapse, maxdepth, shift_toc, root_links)

    if shift_toc:
        update_navtree_classes(navtree)

    return app.builder.render_partial(navtree)['fragment']


def iter_toctree(toctree):
    iterator = iter(toctree)
    caption = None
    while True:
        try:
            top_level_node = next(iterator)
            if isinstance(top_level_node, nodes.bullet_list):
                yield (top_level_node, caption)
                caption = None
            elif isinstance(top_level_node, nodes.caption):
                caption = top_level_node
                continue
            else:
                raise NavtreeError("Expected a 'bullet_list' node, got '%s'"
                                   % top_level_node.__class__.__name__)
        except StopIteration:
            break


def process_toctree_list(navtree, bullet_list, caption, app,
                         collapse, maxdepth, shift_toc, root_links, level=1):

    for list_item in bullet_list.children:

        if len(list_item) == 1: # Just a link, no sublist
            continue
        if len(list_item) != 2:
            raise NavtreeError("Expected 'list_item' with exactly 2 child nodes, got '%s' with %d: %s"
                               % (list_item.__class__.__name__, len(list_item), list_item.children))

        title_node = list_item[0][0]  # list_item > paragraph > reference
        list_node = list_item[1]      # list_item > bullet_list
        if not root_links:
            # Use the `Text` node instead of the enclosing `reference` object.
            title_node = title_node[0]
        if caption:
            prune_depth = maxdepth.get(title_node.astext(),
                                       maxdepth.get(caption.astext(),
                                                    maxdepth['default']))
        else:
            prune_depth = maxdepth.get(title_node.astext(),
                                       maxdepth['default'])

        app.env._toctree_prune(node     = list_item,
                               depth    = level if shift_toc else level + 1,
                               maxdepth = prune_depth,
                               collapse = collapse)

        if shift_toc and level == 1:
            caption = nodes.caption(title_node.astext(), '', title_node)
            if root_links:
                caption['classes'].append('link')
            navtree += caption
            navtree += list_node

        if level < 2:
            process_toctree_list(navtree, list_node, None, app,
                                 collapse, maxdepth, shift_toc, root_links, level=level+1)

    if not shift_toc and level == 1:
        if caption:
            navtree += caption
        navtree += bullet_list


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
    if isinstance(app.builder, SerializingHTMLBuilder):
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

