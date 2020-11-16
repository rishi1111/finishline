import sys
import os
import json
sys.path.append("..")  # comment out if importing from pip module

import dash
from finishline import FinishLine
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.title = "Dash FinishLine"

data = {"state": "Montréal", "country": "Canada"}

from plugins.AddChart import finalize1


def generate_layout(**kwargs):
    if not kwargs.get("path_name"):
        return html.Div(
            [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
        )
    fl = FinishLine(app=app, data=data, debug=False, debug_path=None)
    fl.load_plugins()
    fl.name = kwargs.get("path_name")

    json_path = fl.name
    json_path = json_path.replace("/","") + ".json"
    layouts = {}
    children = []

    if os.path.isfile(json_path):
        with open(json_path, "r") as openfile:
            ls = json.load(openfile)
            children = ls[0]
            layouts = ls[1]

    layouts = fl.generate_layout(layouts=layouts)
    layouts.children[1].children = children

    # import pdb;pdb.set_trace()


    return layouts
# Update the index
@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname != "/":
        return generate_layout(path_name=pathname)
    else:
        return "Welcome, Please add /{datasourceID} to url"
    # You could also return a 404 "URL not found" page here

app.layout = generate_layout
finalize1(app, data, None)


if __name__ == "__main__":
    app.run_server(debug=True, port=5000, host="0.0.0.0")
