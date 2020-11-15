from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc
from chart_factory.chart_factory import create_chart

def initialize(app, data, fl):
    fl.register_vis(
        "Add new chart",
        html.Button('Create New Chart', id='create-chart',n_clicks=0, style={})
    )


def finalize(app, data, fl):
    @app.callback(Output('placeholder', 'children'),
                  [Input('create-chart-2', 'n_clicks')])
    def update_output(n_clicks):
        return f"PLACEHOLDER - add {n_clicks}"

    # @app.callback(Output('create-chart-2', 'n_clicks'),
    #               [Input('create-chart', 'n_clicks')],
    #               [State('create-chart-2', 'n_clicks')])
    # def update_output(n_clicks,nclicks_2):
    #     print("HAHHAHAHAHA")
    #     print(n_clicks,nclicks_2)
    #     return nclicks_2 + 1

    @app.callback(Output('default-fl-page-layout', 'children'),
                  [Input('create-chart', 'n_clicks')],
                  [State('default-fl-page-layout', 'children')])
    def update_output_2(n_clicks,children:list):
        print("children")
        new_card_json = create_chart(fl,random_id = n_clicks)
        children.append(new_card_json)
        return children



