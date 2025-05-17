# This project is a FastAPI service built on top of the pybaseball library:
# https://github.com/jldbc/pybaseball
#
# This service is not affiliated with MLB or the official data sources used by pybaseball.

from pybaseball import statcast

DATASET_REGISTRY = {
    "statcast": {
        "description": "MLB Statcast data from Baseball Savant",
        "tables": {
            "statcast": {
                "function": statcast,
                "description": "Raw Statcast data including pitch-level tracking and batted ball metrics.",
                "params": ["start_dt", "end_dt"],
                "required": ["start_dt", "end_dt"]
            }
        }
    }
}