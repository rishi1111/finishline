import sys

sys.path.append("..")  # comment out if importing from pip module

import dash
from finishline import FinishLine

app = dash.Dash()
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.title = "Dash FinishLine"

data = {"state": "Montréal", "country": "Canada"}

fl = FinishLine(app=app, data=data, debug=False, debug_path=None)
fl.load_plugins()
app.layout = fl.generate_layout(
    layouts={
        "lg": [
            {
                "w": 3,
                "h": 2,
                "x": 0,
                "y": 0,
                "i": "Add new chart",
                "moved": False,
                "static": False,
            },
            {
                "w": 3,
                "h": 3,
                "x": 0,
                "y": 0,
                "i": "US Export of Plastic Scrap",
                "moved": False,
                "static": False,
                "minH": 2,
                "minW": 3,
            },
            {
                "w": 4,
                "h": 2,
                "x": 4,
                "y": 0,
                "i": "US Export of Plastic Scrap-1",
                "moved": False,
                "static": False,
                "minH": 2,
                "minW": 3,
            },
            {
                "w": 4,
                "h": 2,
                "x": 0,
                "y": 2,
                "i": "US Export of Plastic Scrap-2",
                "moved": False,
                "static": False,
                "minH": 2,
                "minW": 3,
            },
        ],
        "md": [],
        "sm": [],
    }
)

if __name__ == "__main__":
    fl.run_server(debug=True, port=5000, host="0.0.0.0")
