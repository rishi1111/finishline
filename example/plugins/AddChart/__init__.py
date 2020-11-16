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

def finalize(app, data, fl):
    pass


def finalize1(app, data, fl):
    @app.callback(
        Output({"type": "fl-card", "index": MATCH}, "children"),
        [Input({"type": "close-btn", "index": MATCH}, "n_clicks"),],
        [
            State({"type": "fl-card", "index": MATCH}, "children"),
            State({"type": "fl-card", "index": MATCH}, "id"),
        ],
        prevent_initial_call=True,
    )
    def confirm_dialog(n_clicks, children, id):
        id = id["index"]
        dropdown = [
            html.Span("Feedback", style={"width": "100%", "text-align": "center"}),
            dcc.Dropdown(
                options=[
                    {"label": "Incorrect Graph Type", "value": "Incorrect Graph Type"},
                    {"label": "Incorrect X-Axis", "value": "Incorrect X-Axis"},
                    {"label": "Incorrect Y-Axis", "value": "Incorrect Y-Axis"},
                ],
                value=[],
                placeholder="Choose Reason(s)",
                multi=True,
                id={"type": "feedback-dropdown", "index": id},
            ),
            html.Button(
                "Submit & Close",
                id={"type": "feedback-btn", "index": id},
                type="submit",
            ),
        ]

        children = [children[0]] + dropdown
        # import pdb;pdb.set_trace()
        return children

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
            Input({"type": "feedback-btn", "index": ALL}, "n_clicks"),
        ],
        [
            State({"type": "page_layout", "index": ALL}, "children"),
            State({"type": "page_layout", "index": ALL}, "layouts"),
            State({"type": "feedback-dropdown", "index": ALL}, "value"),
            #
        ],
        prevent_initial_call=True,
    )
    def update_grid(n_clicks, n_clicks2, children: list, layout, feedback_reasons):
        import pdb;
        # pdb.set_trace()
        if (len(layout) != 1) or (len(children) != 1):
            print("Exception - More than 1 input triggered")
            raise PreventUpdate()
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
        elif action == "feedback-btn" and not n_clicks2[0]:
            # handle case where button event gets triggered # TODO
            raise PreventUpdate()
        else:
            print(
                f"FEEDBACK {feedback_reasons[0]}"
            )  # TODO - crud call for saving feedback
            children, layout = delete_chart(children, layout, index)


        return [children], [layout]
