import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from functions import llm

def register_callbacks(app, model):

    @app.callback(
            [dash.dependencies.Output('system-instructions-store', 'data')],
             [dash.dependencies.Input('system-instructions', 'value')]
    )
    def update_system_instructions(system_instructions):
        if system_instructions:
            return [system_instructions]
        else:
            return [""]






    @app.callback(
        [dash.dependencies.Output("chat-history", "children"),
         dash.dependencies.Output("conversation-history", "data"),
         dash.dependencies.Output("input-box", "value")],
        [dash.dependencies.Input("send-button", "n_clicks"),
         dash.dependencies.Input("input-box", "value")],
        [dash.dependencies.State("conversation-history", "data"),
         dash.dependencies.State("system-instructions-store", "data")]
    )
    def update_chat_history(n_clicks, user_input, store, system_instructions):
        if n_clicks is None or not user_input or n_clicks == store['n_clicks']:
            
            return dash.no_update
        
        # Append this to the conversation history
        store['conv'].append( html.P("User: " + user_input))
        model.set_system_instructions(system_instructions)
        # compute the output from LLM in memory
        output = model.chat(user_input)
        
        # Append this to the conversation history
        store['conv'].append( dcc.Markdown("Agent: " + output))

        #response = f"Agent: {user_input}"
        store['n_clicks'] += 1

        # Format the Conversation History Properly
        return_list = []
        for message, next_message in zip(store['conv'][0::2], store['conv'][1::2]):
            print(message)
            temp_card = dbc.Card([
                message,
                next_message
            ], className = 'card-with-padding')
            return_list.append(temp_card)
        return_to_label = html.Div(return_list)
        return return_to_label, store, ""
    