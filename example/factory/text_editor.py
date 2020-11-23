fig.update_layout(
    grid={"rows": 1, "columns": 1, "pattern": "independent"},
    template={
        "data": {
            "indicator": [
                {
                    "mode": "number+delta",
                    "delta": {"reference": 90},
                }
            ]
        }
    },
)
