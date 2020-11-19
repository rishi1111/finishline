# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent
import json
import dash_responsive_grid_layout as dgl
import copy

def merge(a, b):
    return dict(a, **b)


def omit(omitted_keys, d):
    return {k: v for k, v in d.items() if k not in omitted_keys}


def Page(children=None, **kwargs):
    return html.Div(
        children,
        className='fl-page',
        **kwargs
    )


def Layout(children=None, layouts=None, cols=None, rowHeight=100, **kwargs):

    layouts = layouts or {'lg':[], 'md':[], 'sm':[] }
    cols = cols or { 'lg': 12, 'md': 6, 'sm': 2 }
    # import pdb;pdb.set_trace()

    return dgl.ResponsiveGridLayout(
        children,
        layouts=layouts,
        cols=cols,
        rowHeight=rowHeight,
        draggableHandle='.fl-titlebar',
        draggableCancel=".fl-x-mark",
        verticalCompact=True,
        **kwargs
    )


def Card(children, title, card_id, story_id, href=None, **kwargs):
    t = [html.A(title, href=href, target=title), html.Button("X",className="fl-x-mark", id={"type":"close-btn","index":story_id, "id":card_id})]
    if isinstance(children, dcc.Graph):
        # note: don't put children in a div container wrapper, else plotly won't resize properly
        c = [html.Div(t, className='fl-titlebar')] + [children]
    else:
        c = [html.Div(t, className='fl-titlebar'), html.Div(children, className='fl-content')]


    return html.Div(
        c,
        className='fl-card',
        id={"type":"fl-card","index":story_id, "id":card_id},
        style=merge({}, kwargs.get('style', {})),
        **omit(['style'], kwargs)
    )