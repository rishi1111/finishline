from dash.dependencies import Output, Input, ALL, State, MATCH, ALLSMALLER
import dash_html_components as html
import dash_core_components as dcc
from dash import callback_context
from factory.chart_factory import create_chart, delete_chart,update_figure
from factory.filters import create_filter, delete_filter, toggle_selected_column
import json
from dash.exceptions import PreventUpdate
from datetime import datetime
import pandas as pd


def finalize1(app, data, fl):
    @app.callback(
        Output({"type": "dynamic-chart", "index": ALL, "id": ALL}, "figure"),
        [Input({"type": "signal", "index": ALL}, "children")],
        [State({"type": "dynamic-chart", "index": ALL, "id": ALL}, "figure"),
         State({"type": "dynamic-chart", "index": ALL, "id": ALL}, "id")],
        prevent_initial_call=True,
    )
    def update_chart_filter(name,figures,figure_id):
        print(name)
        df = pd.read_feather(f"{name[0]}.feather")


        charts_config = []
        newfigs = []
        ls = callback_context.triggered
        import pdb;
        # pdb.set_trace()

        for fig in figures:

            x = {"type":fig["data"][0]["type"],
             "xaxis":fig["layout"]["xaxis"]["title"]["text"],
             "yaxis": fig["layout"]["yaxis"]["title"]["text"]
             }
            import pdb;
            # pdb.set_trace()
            newfig = update_figure(df,xaxis=x["xaxis"],yaxis=x["yaxis"],chart_type=x["type"])
            newfigs.append(newfig)

        print(charts_config)



        return newfigs
        # create_chart()
        # raise PreventUpdate()



    @app.callback(
        Output({"type": "signal", "index": ALL,}, "children"),
        [Input({"type": "dynamic-dpn-column", "index": ALL, "id": ALL}, "value"),],
        [State({"type": "page_layout", "index": ALL}, "id"),
         State({"type": "dynamic-dpn-column-label", "index": ALL, "id": ALL}, "children"),
         ],
        prevent_initial_call=True,
    )
    def dynamic_filter(column_value, story_board_id,label_list):
        # import pdb;pdb.set_trace()
        if (len(story_board_id) != 1) or not column_value:
            print("Exception - More than storyboard - " + str(story_board_id))
            raise PreventUpdate()
        else:

            payload = {}
            for i,label in enumerate(label_list):
                payload[label[0]] = column_value[i]

            story_board_id = story_board_id[0]["index"].replace("/", "")
            ls = callback_context.triggered
            index = ls[0]["prop_id"]
            if index == ".":
                import pdb;pdb.set_trace()
                # raise PreventUpdate()
                pass
            else:
                component = json.loads(index.rsplit(".")[0])
                index = component["index"]
                action = component["type"]

        # print(index)
        print("payload",payload)
        # df = pd.DataFrame({"abc": [1, 2, 3, 4, 5, 6]})
        df = pd.read_feather(f"sales.feather")
        ser = pd.Series(True, index=df.index)
        for x in payload:
            if payload[x]:
                ser = ser & df[x].isin(payload[x])
        df = df[ser].reset_index(drop=True)

        df.reset_index(drop=True).to_feather(f"{story_board_id}.feather")

        return [story_board_id]

    @app.callback(
        [
            Output({"type": "global-filter-listing", "index": ALL,}, "children"),
            Output({"type": "create-filter-dpn", "index": ALL}, "options"),
            Output({"type": "create-filter-dpn", "index": ALL}, "value"),
        ],
        [
            Input({"type": "create-filter-btn", "index": ALL}, "n_clicks"),
            Input({"type": "close-filter-btn", "index": ALL, "id": ALL, "column_name":ALL}, "n_clicks"),
        ],
        [
            State({"type": "create-filter-dpn", "index": ALL}, "value"),
            State({"type": "global-filter-listing", "index": ALL}, "children"),
            State({"type": "create-filter-dpn", "index": ALL}, "options"),
        ],
        prevent_initial_call=True,
    )
    def global_filter_crud(
        n_clicks, n_clicks2, column_name, filter_list: list, column_options):

        if (
            (len(column_name) != 1)
            or (len(filter_list) != 1)
            or len(column_options) != 1
        ):
            print("Exception - More than 1 input triggered")

            raise PreventUpdate()
        else:
            filter_list = filter_list[0]
            column_name = column_name[0]
            column_options = column_options[0]

            print(column_options)

        ls = callback_context.triggered
        # import pdb;pdb.set_trace()
        index = ls[0]["prop_id"]
        component = json.loads(index.rsplit(".")[0])

        storyid = component["index"]
        action = component["type"]

        if action == "create-filter-btn":
            if not column_name:  # empty input
                raise PreventUpdate()
            import random

            random_id = int(random.random() * 100) + 100
            filter_card = create_filter(
                column_name=column_name,
                options=[],
                storyid=storyid,
                filterid=random_id,
            )
            filter_list.append(filter_card)
            column_options = toggle_selected_column(
                column_options, column_name, disabled=True
            )
        else:
            # import pdb;pdb.set_trace()
            filter_list = delete_filter(component["id"], filter_list)
            column_options = toggle_selected_column(
                column_options, component["column_name"], disabled=False
            )

        return [filter_list], [column_options], [None]

    @app.callback(
        Output({"type": "fl-card", "index": MATCH, "id": MATCH}, "children"),
        [Input({"type": "close-btn", "index": MATCH, "id": MATCH}, "n_clicks"),],
        [
            State({"type": "fl-card", "index": MATCH, "id": MATCH}, "children"),
            State({"type": "fl-card", "index": MATCH, "id": MATCH}, "id"),
        ],
        prevent_initial_call=True,
    )
    def confirm_dialog(n_clicks, children, id):

        storyid = id["index"]
        chartid = id["id"]

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
                id={"type": "feedback-dropdown", "index": storyid, "id": chartid},
            ),
            html.Button(
                "Submit & Close",
                id={"type": "feedback-btn", "index": storyid, "id": chartid},
                type="submit",
            ),
        ]

        children = [children[0]] + dropdown
        return children

    @app.callback(
        Output({"type": "placeholder", "index": MATCH}, "children"),
        [Input({"type": "save-grid-btn", "index": MATCH}, "n_clicks")],
        [
            State({"type": "page_layout", "index": MATCH}, "children"),
            State({"type": "page_layout", "index": MATCH}, "layouts"),
            State({"type": "page_layout", "index": MATCH}, "id"),
            State({"type": "page_header", "index": MATCH}, "children"),
        ],
        prevent_initial_call=True,
    )
    def update_output(n_clicks, children, layout, index,page_header):
        # import pdb;pdb.set_trace()
        index = index["index"].replace("/", "")

        # Writing to sample.json {"type": "page_header", "index": unique_name}

        with open(f"{index}.json", "w+") as outfile:
            ls = json.load(outfile)
            json_object = json.dumps((children, layout, page_header))
            outfile.write(json_object)

        return f'Placeholder - Last Saved at {datetime.now().strftime("%I:%M:%S %p")}'

    @app.callback(
        [
            Output({"type": "page_layout", "index": ALL}, "children"),
            Output({"type": "page_layout", "index": ALL}, "layouts"),
        ],
        [
            Input({"type": "create-chart-btn", "index": ALL}, "n_clicks"),
            Input({"type": "feedback-btn", "index": ALL, "id": ALL}, "n_clicks"),
        ],
        [
            State({"type": "page_layout", "index": ALL}, "children"),
            State({"type": "page_layout", "index": ALL}, "layouts"),
            State({"type": "feedback-dropdown", "index": ALL, "id": ALL}, "value"),
            #
        ],
        prevent_initial_call=True,
    )
    def update_grid(n_clicks, n_clicks2, children: list, layout, feedback_reasons):

        if (len(layout) != 1) or (len(children) != 1):
            print("Exception - More than 1 input triggered")

            raise PreventUpdate()
        else:
            children = children[0]
            layout = layout[0]

        ls = callback_context.triggered
        index = ls[0]["prop_id"]
        component = json.loads(index.rsplit(".")[0])

        storyid = component["index"]
        action = component["type"]

        if action == "create-chart-btn":
            import random

            random_id = int(random.random() * 100) + 100
            new_card_json, card_layout = create_chart(storyid, chart_id=random_id)
            children.append(new_card_json)
            layout["lg"].append(card_layout)
        elif action == "feedback-btn" and not n_clicks2[0]:
            # handle case where button event gets triggered # TODO
            raise PreventUpdate()
        else:
            print(
                f"FEEDBACK {feedback_reasons[0]}"
            )  # TODO - crud call for saving feedback
            children, layout = delete_chart(children, layout, storyid)

        return [children], [layout]
