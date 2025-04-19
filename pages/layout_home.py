import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


layout = dbc.Container(
    [
        dbc.Navbar("The Imitation Engine", className="navbar-text", color="dark", dark=True),
        html.Br(),
        dbc.Row(
            [
                    dbc.Container([
                        dbc.Card(
                        [   dcc.Store(id = 'system-instructions-store', data=[""]),
                            dbc.CardHeader("System Instruction", className="generic-bold-text"),
                            dbc.CardBody([
                                dbc.Input(id = 'system-instructions', type = 'text', placeholder = "System Instructions"),]
                                ),
                            ], className="llm-selection-card-body")
                        ], 
                     fluid = True)
            ]
        ),
        html.Br(),

        dbc.Row(
            [
                dbc.Container([
                    dbc.Card(
                        [dcc.Store(id="conversation-history", data={'n_clicks': 0, 'conv': []}),
                            dbc.CardHeader("Chat History", className="generic-bold-text"),
                         dbc.CardBody(
                             [
                                 html.P("Agent: Hi How may I help you?", className = "generic-bold-text", id = "chat-history"),
                             ]
                         ),
                         ], className = "scrollable-card",
                        ), 
                        html.Br(),
                        dbc.InputGroup(
                             [
                                 dbc.Input(id="input-box", placeholder="User Prompt", type="text"),
                                 dbc.Button("Send", id="send-button", color="primary")
                             ]
                         )], fluid = True)
                ])
            ]
        )

