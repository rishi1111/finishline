from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc


def initialize(app, data, fl):
    pass
    # chart_title = "US Export of Plastic Scrap"
    # chart_title_1 = "US Export of Plastic Scrap-1"
    # chart_title_2 = "US Export of Plastic Scrap-2"
    #
    # chart_id = "chart-id-1"
    # chart_id_2 = "chart-id-2"
    # chart_id_3 = "chart-id-3"
    #
    # fl.register_vis(
    #     chart_title,
    #     dcc.Graph(
    #         figure=dict(
    #             data=[
    #                 dict(
    #                     x=[
    #                         1995,
    #                         1996,
    #                         1997,
    #                         1998,
    #                         1999,
    #                         2000,
    #                         2001,
    #                         2002,
    #                         2003,
    #                         2004,
    #                         2005,
    #                         2006,
    #                         2007,
    #                         2008,
    #                         2009,
    #                         2010,
    #                         2011,
    #                         2012,
    #                     ],
    #                     y=[
    #                         219,
    #                         146,
    #                         112,
    #                         127,
    #                         124,
    #                         180,
    #                         236,
    #                         207,
    #                         236,
    #                         263,
    #                         350,
    #                         430,
    #                         474,
    #                         526,
    #                         488,
    #                         537,
    #                         500,
    #                         439,
    #                     ],
    #                     name="Rest of world",
    #                     marker=dict(color="rgb(55, 83, 109)"),
    #                 ),
    #                 dict(
    #                     x=[
    #                         1995,
    #                         1996,
    #                         1997,
    #                         1998,
    #                         1999,
    #                         2000,
    #                         2001,
    #                         2002,
    #                         2003,
    #                         2004,
    #                         2005,
    #                         2006,
    #                         2007,
    #                         2008,
    #                         2009,
    #                         2010,
    #                         2011,
    #                         2012,
    #                     ],
    #                     y=[
    #                         16,
    #                         13,
    #                         10,
    #                         11,
    #                         28,
    #                         37,
    #                         43,
    #                         55,
    #                         56,
    #                         88,
    #                         105,
    #                         156,
    #                         270,
    #                         299,
    #                         340,
    #                         403,
    #                         549,
    #                         499,
    #                     ],
    #                     name="China",
    #                     marker=dict(color="rgb(26, 118, 255)"),
    #                 ),
    #             ],
    #             layout=dict(
    #                 showlegend=True,
    #                 legend=dict(x=0, y=1.0),
    #                 margin=dict(l=40, r=0, t=40, b=30),
    #             ),
    #         ),
    #         style={"height": "90%"},
    #         id=chart_id,
    #         responsive=True,
    #         config={
    #             "autosizable": True,
    #             "doubleClick": "autosize",
    #             "frameMargins": 0,
    #             "responsive": True,
    #             "watermark":False
    #         },
    #     ),
    # )
    #
    # fl.register_vis(
    #     chart_title_1,
    #     dcc.Graph(
    #         figure=dict(
    #             data=[
    #                 dict(
    #                     x=[
    #                         1995,
    #                         1996,
    #                         1997,
    #                         1998,
    #                         1999,
    #                         2000,
    #                         2001,
    #                         2002,
    #                         2003,
    #                         2004,
    #                         2005,
    #                         2006,
    #                         2007,
    #                         2008,
    #                         2009,
    #                         2010,
    #                         2011,
    #                         2012,
    #                     ],
    #                     y=[
    #                         219,
    #                         146,
    #                         112,
    #                         127,
    #                         124,
    #                         180,
    #                         236,
    #                         207,
    #                         236,
    #                         263,
    #                         350,
    #                         430,
    #                         474,
    #                         526,
    #                         488,
    #                         537,
    #                         500,
    #                         439,
    #                     ],
    #                     name="Rest of world",
    #                     marker=dict(color="rgb(55, 83, 109)"),
    #                 ),
    #                 dict(
    #                     x=[
    #                         1995,
    #                         1996,
    #                         1997,
    #                         1998,
    #                         1999,
    #                         2000,
    #                         2001,
    #                         2002,
    #                         2003,
    #                         2004,
    #                         2005,
    #                         2006,
    #                         2007,
    #                         2008,
    #                         2009,
    #                         2010,
    #                         2011,
    #                         2012,
    #                     ],
    #                     y=[
    #                         16,
    #                         13,
    #                         10,
    #                         11,
    #                         28,
    #                         37,
    #                         43,
    #                         55,
    #                         56,
    #                         88,
    #                         105,
    #                         156,
    #                         270,
    #                         299,
    #                         340,
    #                         403,
    #                         549,
    #                         499,
    #                     ],
    #                     name="China",
    #                     marker=dict(color="rgb(26, 118, 255)"),
    #                 ),
    #             ],
    #             layout=dict(
    #                 showlegend=True,
    #                 legend=dict(x=0, y=1.0),
    #                 margin=dict(l=40, r=0, t=40, b=30),
    #             ),
    #         ),
    #         style={"height": "90%"},
    #         id=chart_id_2,
    #     ),
    # )
    # fl.register_vis(
    #     chart_title_2,
    #     dcc.Graph(
    #         id=chart_id_3,
    #         style={"height": "90%"},
    #         figure={
    #             "data": [
    #                 {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
    #                 {
    #                     "x": [1, 2, 3],
    #                     "y": [2, 4, 5],
    #                     "type": "bar",
    #                     "name": u"Montréal",
    #                 },
    #             ],
    #             "layout": dict(
    #                 showlegend=True,
    #                 legend=dict(x=0, y=1.0),
    #                 margin=dict(l=40, r=0, t=40, b=30),
    #             ),
    #         },
    #     ),
    # )


def finalize(app, data, fl):
    pass
