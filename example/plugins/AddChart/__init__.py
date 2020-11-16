from dash.dependencies import Output, Input, ALL, State, MATCH, ALLSMALLER
import dash_html_components as html
import dash_core_components as dcc
from dash import callback_context
from chart_factory.chart_factory import create_chart, delete_chart
import json
from dash.exceptions import PreventUpdate
from datetime import datetime


def initialize(app, data, fl):
    pass
    # fl.register_vis(
    #     "Add new chart",
    #     html.Button("Create New Chart", id="create-chart", n_clicks=0, style={}),
    # )


def finalize(app, data, fl):
    pass


def finalize1(app, data, fl):
    @app.callback(
        Output({"type": "placeholder", "index": MATCH}, "children"),
        [Input({"type": "save-grid-btn", "index": MATCH}, "n_clicks")],
        [
            State({"type": "page_layout", "index": MATCH}, "children"),
            State({"type": "page_layout", "index": MATCH}, "layouts"),
            State({"type": "page_layout", "index": MATCH}, "id"),
        ],
        prevent_initial_call=True,
    )
    def update_output(n_clicks, children, layout, index):
        index = index["index"].replace("/", "")
        json_object = json.dumps((children, layout))
        # Writing to sample.json

        with open(f"{index}.json", "w") as outfile:
            outfile.write(json_object)

        return f'Placeholder - Last Saved at {datetime.now().strftime("%I:%M:%S %p")}'

    @app.callback(
        [
            Output({"type": "page_layout", "index": ALL}, "children"),
            Output({"type": "page_layout", "index": ALL}, "layouts"),
        ],
        [
            Input({"type": "create-chart-btn", "index": ALL}, "n_clicks"),
            Input({"type": "close-btn", "index": ALL}, "n_clicks"),
        ],
        [
            State({"type": "page_layout", "index": ALL}, "children"),
            State({"type": "page_layout", "index": ALL}, "layouts"),
        ],
        prevent_initial_call=True,
    )
    def update_grid(n_clicks, n_clicks2, children: list, layout):
        if (len(layout) != 1) or (len(children) != 1):
            print("Exception - More than 1 input triggered")
            raise PreventUpdate()
        # delete card {"index":"US Export of Plastic Scrap-101","type":"close-btn"}
        children = children[0]
        layout = layout[0]

        ls = callback_context.triggered
        index = ls[0]["prop_id"]
        component = json.loads(index.rsplit(".")[0])
        index = component["index"]
        action = component["type"]

        if action == "create-chart-btn":
            new_card_json, card_layout = create_chart(fl, random_id=n_clicks[0])
            children.append(new_card_json)
            layout["lg"].append(card_layout)
        else:
            import pdb

            # pdb.set_trace()

            children, layout = delete_chart(children, layout, index)
            # import pdb;pdb.set_trace()

        # add new card

        return [children], [layout]
        # return children
