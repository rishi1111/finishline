from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc
import finishline.grid_components as gc
import json
import plotly
import random
import dash_bootstrap_components as dbc


def toggle_selected_column(column_options:list, column_name:str, disabled:bool)->list:
    for option in column_options:
        if option["value"] == column_name:
            option["disabled"] = disabled

    return column_options


def create_filter(column_name:str, options,storyid,filterid):
    random_id = int(random.random() * 100) + 100
    filter_card = dbc.Col(
        [
            dbc.Label([column_name], style={"margin-bottom": "0px"},id={"type": "dynamic-dpn-column-label", "index": storyid, "id":filterid}),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            multi=True,
                            options=options,
                            value=[],
                            placeholder="Choose Value(s)",
                            id={"type": "dynamic-dpn-column", "index": storyid, "id":filterid}
                        ),
                        width="10",
                        style={"padding-right": "0px"},


                    ),
                    dbc.Col(
                        html.Button(
                            "X",
                            id={"type": "close-filter-btn", "index": storyid, "id":filterid},
                            style={"margin": "5px","border": "0px","cursor":"pointer"}
                        )
                        ,width="1",
                        style={"padding-left":"1px"}
                    ),
                ]
            ),
        ],
        width="3",
        style={"margin-bottom": "10px"},
        id={"type": "filter-card", "index": storyid, "id":filterid},
    )

    return filter_card.to_plotly_json()


def delete_filter(index,filter_list):

    ls_index = -1
    for idx,filter_card in enumerate(filter_list):
        if filter_card["props"]["id"]["index"] == index:
            ls_index = idx

    if ls_index != -1:
        filter_list.pop(ls_index)
    return filter_list


