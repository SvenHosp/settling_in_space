# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Settling in Space'),

    html.Div(children='''
        A game about settling in the space.
    '''),

    html.Button('configure', id='configure', n_clicks=0),
    html.Button('initialize', id='initialize', n_clicks=0),
    html.Button('start', id='start', n_clicks=0),
    html.Div('status game server', id='gameserveroutput')
])

@app.callback(
    dash.dependencies.Output('gameserveroutput', 'children'),
    [dash.dependencies.Input('configure', 'n_clicks'),
     dash.dependencies.Input('initialize', 'n_clicks'),
     dash.dependencies.Input('start', 'n_clicks')])
def start_gameserver(btn1, btn2, btn3):
    import xmlrpc.client
    msg = ''
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'configure' in changed_id:
        with xmlrpc.client.ServerProxy("http://rpcgame:8082") as proxy:
            proxy.configure()
        msg = 'game configured (default)'
    elif 'initialize' in changed_id:
        with xmlrpc.client.ServerProxy("http://rpcgame:8082") as proxy:
            proxy.initialize()
        msg = 'game initialized and is now ready'
    elif 'start' in changed_id:
        with xmlrpc.client.ServerProxy("http://rpcgame:8082") as proxy:
            proxy.start()
        msg = 'game started'

    return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')