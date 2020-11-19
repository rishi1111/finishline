import importlib.util
import glob
import os.path
import sys
import traceback
import dash_bootstrap_components as dbc

import finishline.grid_components as gc

import dash

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_building_blocks as dbb
import random
import json
from dash.exceptions import PreventUpdate


class FinishLine(object):
    def __init__(
        self,
        app=None,
        data=None,
        name="default",
        debug=False,
        on_layout_change=None,
        debug_path=None,
    ):

        self.name = name

        # server side
        self.app = app or dash.Dash()
        self.data = data or {}
        self.plugins = {}
        self.blocks = BlockManager()
        self.store = FinishStore(app, hide=(not debug))

        # client side
        self.client_vis = {}
        self.client_data = {}

        # misc
        self.extra_files = []
        self.debug = debug
        self.debug_path = debug_path

        # private
        self._curr_file = None

        # callbacks
        self.on_layout_change = on_layout_change or (lambda lo: print("layout", lo))

    def register_vis(self, name, layout):

        self.client_vis[name] = {"layout": layout, "src_file": self._curr_file}

    def register_data(self, name, inputs=None, state=None, data=None, on_update=None):

        self.client_data[name] = {"data": data or {}, "src_file": self._curr_file}

        ret = self.store.register(name, inputs=inputs, state=state, initially=data)

        if on_update:

            @self.app.callback(
                Output(self.store.ids[name], "role"), [self.store.input(name)]
            )
            def data_callback(new_data):
                on_update(json.loads(new_data))
                raise PreventUpdate()

        return ret

    def generate_layout(self, components=gc, layouts=None, cols=None):
        unique_name = self.name

        # client side data objects
        c_data_style = {"display": "block"} if self.debug_path else {"display": "none"}
        c_data = self.store.debug_layout(self.client_data)

        # c_vis = self._gen_c_vis(components, layouts)
        c_vis = []
        layout = components.Page(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Button(
                                            "Create New Chart",
                                            id={
                                                "type": "create-chart-btn",
                                                "index": unique_name,
                                            },
                                            style={},
                                            n_clicks=0,
                                        ),
                                    ],
                                    width="2",
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        options=[],
                                                        value=[],
                                                        placeholder="Select a column",
                                                        id={
                                                            "type": "create-filter-dpn",
                                                            "index": unique_name,
                                                        }
                                                        # style={"float":"left","width": "60%"}
                                                    )
                                                ),
                                                dbc.Col(
                                                    html.Button(
                                                        "Add filter",
                                                        id={
                                                            "type": "create-filter-btn",
                                                            "index": unique_name,
                                                        },
                                                        # style={"float":"right","width":"30%"},
                                                        n_clicks=0,
                                                    )
                                                ),
                                            ]
                                        ),
                                    ],
                                    width="5",
                                ),
                                dbc.Col(
                                    [
                                        html.Span(
                                            "PLACEHOLDER FOR DROPPABLE CHARTS",
                                            id={
                                                "type": "placeholder",
                                                "index": unique_name,
                                            },
                                        )
                                    ],
                                    width=True,
                                ),
                                dbc.Col(
                                    [
                                        html.Button(
                                            "SAVE GRID",
                                            id={
                                                "type": "save-grid-btn",
                                                "index": unique_name,
                                            },
                                            style={"float": "right"},
                                            n_clicks=0,
                                        )
                                    ],
                                    width="1",
                                ),
                            ],
                            style={"border-bottom": "5px solid black"},
                        ),
                        dbc.Row(
                            [],
                            style={"padding": "10px"},
                            id={"type": "global-filter-listing", "index": unique_name,},
                        ),
                    ],
                    id={"type": "page_header", "index": unique_name},
                ),
                components.Layout(
                    c_vis,
                    id={"type": "page_layout", "index": unique_name},
                    layouts=layouts,
                    cols=cols,
                ),
                html.Div(
                    c_data,
                    className="fl-data",
                    id={"type": "page_data", "index": unique_name},
                    style=c_data_style,
                ),
                html.Div(
                    id={"type": "signal", "index": unique_name},
                    style={"display": "none"},
                ),
            ],
            id={"type": "page_id", "index": unique_name},
        )

        # run plugin finalize method, e.g. should be used to create callbacks
        self._finalize()

        return layout

    # def _gen_c_vis(self, components, layouts):
    #     i = 0
    #     c = []
    #     ii = [l["i"] for l in layouts["lg"]] if (layouts and "lg" in layouts) else []
    #     for (name, vis) in self.client_vis.items():
    #         key = str(i) if str(i) in ii else name
    #         key = name if name in ii else key
    #         c.append(
    #             components.Card(vis["layout"], title=name, i=key, href=vis["src_file"])
    #         )
    #         i = i + 1
    #
    #     return c

    # def load_plugins(self, plugins_path="plugins/*"):
    #
    #     modules = sorted(glob.glob(plugins_path))
    #
    #     for m in modules:
    #         #             print(m)
    #         fname = m + "/__init__.py"
    #         if not os.path.isfile(fname):
    #             continue
    #
    #         if self.debug_path is not None:
    #             self._curr_file = os.path.abspath(fname).replace(
    #                 self.debug_path["root"], self.debug_path["target"]
    #             )
    #
    #         self.extra_files.append(fname)  # TODO walk all py files in dir
    #         spec = importlib.util.spec_from_file_location(m, fname)
    #         #             print(spec)
    #         plugin = importlib.util.module_from_spec(spec)
    #
    #         try:
    #             spec.loader.exec_module(plugin)
    #             plugin.initialize(self.app, self.data, self)
    #         except:
    #             traceback.print_exc()
    #             print("Unexpected error in plugin, ", m, ": ", sys.exc_info()[0])
    #             self.register_vis(
    #                 m,
    #                 html.Pre(
    #                     "Unexpected error in " + m + "\n" + traceback.format_exc()
    #                 ),
    #             )
    #             # TODO: register 'XXX' instead of 'plugin/XXX'
    #
    #         self.plugins[m] = plugin

    def _finalize(self):
        for plugin in self.plugins.values():
            if "finalize" in plugin.__dict__:
                plugin.finalize(self.app, self.data, self)

    def run_server(self, port=5000, debug=False, **flask_run_options):
        self.app.run_server(
            port=port, debug=debug, extra_files=self.extra_files, **flask_run_options
        )


class FinishStore(dbb.Store):
    def debug_layout(self, client_data):
        style = {"display": "none"} if self.hide else None
        return html.Div(
            [
                html.Div(
                    [
                        html.A(children=[k + ":"], href=v["src_file"], target=k),
                        html.Div(json.dumps(v["data"]), id=self.ids[k]),
                    ]
                )
                for k, v in client_data.items()
            ]
        )


class BlockManager:
    def __init__(self):
        self._blocks = {}

    def register(self, name, block):
        self._blocks[name] = block

    def __getitem__(self, name):
        return self._blocks[name]

    def __getattr__(self, name):
        return self._blocks[name]
