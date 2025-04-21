import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import json
import diskcache
import os
from pages import layout_home
from pages import callbacks_home
from functions import llm
import logging
import subprocess
import time
import warnings

warnings.filterwarnings('ignore')
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

path = os.path.dirname(os.path.abspath(__file__))
cache = diskcache.Cache(path + '/cache')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "The Imitation Engine"
server = app.server

_model_loaded = False
model = None
@app.server.before_request
def _ensure_model_loaded():
    global _model_loaded
    if not _model_loaded:
        logger.info("Loading model for the first time")
        model = llm.LLM("")
        model.load_llm()
        _model_loaded = True
        logger.info("Loaded model Successfully")
        callbacks_home.register_callbacks(app, model)

app.config.suppress_callback_exceptions = True
app.layout = layout_home.layout


def start_ollama_serve_background():
    # Start ollama serve in the background
    # Start ollama serve in the background
    logger.info("Starting OLLAMA Server")
    proc = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    logger.info(f"Ollama serve started with PID {proc.pid}")
    return proc

if __name__ == "__main__":
    proc = start_ollama_serve_background()
    time.sleep(4)
    # Determine if we are in the real Flask child process
    flask_main = os.environ.get("WERKZEUG_RUN_MAIN") == "true"
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"

    # Start Ollama only once, in child server or when debug is off
    if flask_main or not debug_mode:
        ollama_proc = start_ollama_serve_background()
    else:
        ollama_proc = None

    """ try:
        logger.info("Starting Dash app on port 8050...")
        app.run_server(debug=True, port=8050, threaded=False, use_reloader =True)
    finally:
        logger.info("Terminating OLLAMA Server")
        proc.terminate()
        logger.info("Terminated OLLAMA Server") """
    app.run_server(debug=True, port=8050, threaded=False, use_reloader =True)







