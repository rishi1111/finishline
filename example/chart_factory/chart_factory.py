from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc
import finishline.grid_components as gc


def create_chart(fl,chart_title=None,chart_id=None,random_id=10):
    random_id=random_id+100
    chart_title = f"US Export of Plastic Scrap-{random_id}"
    chart_title_1 = "US Export of Plastic Scrap-1"
    chart_title_2 = "US Export of Plastic Scrap-2"

    chart_id = f"chart-id-{random_id}"
    chart_id_2 = "chart-id-2"
    chart_id_3 = "chart-id-3"


    graph = dcc.Graph(
            figure=dict(
                data=[
                    dict(
                        x=[
                            1995,
                            1996,
                            1997,
                            1998,
                            1999,
                            2000,
                            2001,
                            2002,
                            2003,
                            2004,
                            2005,
                            2006,
                            2007,
                            2008,
                            2009,
                            2010,
                            2011,
                            2012,
                        ],
                        y=[
                            219,
                            146,
                            112,
                            127,
                            124,
                            180,
                            236,
                            207,
                            236,
                            263,
                            350,
                            430,
                            474,
                            526,
                            488,
                            537,
                            500,
                            439,
                        ],
                        name="Rest of world",
                        marker=dict(color="rgb(55, 83, 109)"),
                    ),
                    dict(
                        x=[
                            1995,
                            1996,
                            1997,
                            1998,
                            1999,
                            2000,
                            2001,
                            2002,
                            2003,
                            2004,
                            2005,
                            2006,
                            2007,
                            2008,
                            2009,
                            2010,
                            2011,
                            2012,
                        ],
                        y=[
                            16,
                            13,
                            10,
                            11,
                            28,
                            37,
                            43,
                            55,
                            56,
                            88,
                            105,
                            156,
                            270,
                            299,
                            340,
                            403,
                            549,
                            499,
                        ],
                        name="China",
                        marker=dict(color="rgb(26, 118, 255)"),
                    ),
                ],
                layout=dict(
                    showlegend=True,
                    legend=dict(x=0, y=1.0),
                    margin=dict(l=40, r=0, t=40, b=30),
                ),
            ),
            style={"height": "90%"},
            id=chart_id,
            responsive=True,
            config={
                "autosizable": True,
                "doubleClick": "autosize",
                "frameMargins": 0,
                "responsive": True,
                "watermark": False
            },
        )

    fl.register_vis(
        chart_title,
        graph,
    )
    card = gc.Card(graph, title=chart_title, i=chart_title)
    card_json = card.to_plotly_json()
    ls = card_json["props"]["children"]
    ls2 = [x.to_plotly_json() for x in ls]
    card_json["props"]["children"] = ls2
    return card_json