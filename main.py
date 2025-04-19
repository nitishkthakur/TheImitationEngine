import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import diskcache
import os
from pages import layout_home
from pages import callbacks_home
from functions import llm
import logging

path = os.path.dirname(os.path.abspath(__file__))
cache = diskcache.Cache(path + '/cache')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "The Imitation Engine"

_model_loaded = False
model = None
@app.server.before_request
def _ensure_model_loaded():
    global _model_loaded
    if not _model_loaded:
        model = llm.LLM("")
        model.load_llm()
        _model_loaded = True
        callbacks_home.register_callbacks(app, model)

app.config.suppress_callback_exceptions = True
app.layout = layout_home.layout




if __name__ == "__main__":
    app.run_server(debug=True, port=8050,  threaded=True)





