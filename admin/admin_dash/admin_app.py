# -*- coding: utf-8 -*-
import logging
import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Welcome to admin dashboard'),
    html.Button('start gameserver', id='startgameserver', n_clicks=0),
    html.Button('stop gameserver', id='stopgameserver', n_clicks=0),
    html.Div('status game server', id='gameserveroutput'),
    html.Button('start webpageserver', id='startwebpageserver', n_clicks=0),
    html.Button('stop webpageserver', id='stopwebpageserver', n_clicks=0),
    html.Div('status webpage server', id='webpageserveroutput')
])


@app.callback(
    dash.dependencies.Output('gameserveroutput', 'children'),
    [dash.dependencies.Input('startgameserver', 'n_clicks'),
     dash.dependencies.Input('stopgameserver', 'n_clicks')])
def start_gameserver(btn1, btn2):
    import xmlrpc.client
    msg = ''
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'startgameserver' in changed_id:
        with xmlrpc.client.ServerProxy("http://rpcgame:8088") as proxy:
            proxy.start_gameserver()
        msg = 'game server started'
    elif 'stopgameserver' in changed_id:
        with xmlrpc.client.ServerProxy("http://rpcgame:8088") as proxy:
            proxy.stop_gameserver()
        msg = 'game server stopped'

    return html.Div(msg)

@app.callback(
    dash.dependencies.Output('webpageserveroutput', 'children'),
    [dash.dependencies.Input('startwebpageserver', 'n_clicks'),
     dash.dependencies.Input('stopwebpageserver', 'n_clicks')])
def start_gameserver(btn1, btn2):
    import xmlrpc.client
    msg = ''
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'startwebpageserver' in changed_id:
        with xmlrpc.client.ServerProxy("http://dash:8088") as proxy:
            proxy.start_webpageserver()
        msg = 'webpage server started'
    elif 'stopwebpageserver' in changed_id:
        with xmlrpc.client.ServerProxy("http://dash:8088") as proxy:
            proxy.stop_webpageserver()
        msg = 'webpage server stopped'

    return html.Div(msg)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)