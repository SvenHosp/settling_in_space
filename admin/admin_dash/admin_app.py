# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Welcome to admin dashboard'),
    html.Button('(re)start gameserver', id='switchgameserver'),
    html.Div('', id='gameserveroutput')
])


@app.callback(
    dash.dependencies.Output('gameserveroutput', 'children'),
    [dash.dependencies.Input('switchgameserver', 'children')])
def start_gameserver(btn1):
    import xmlrpc.client

    with xmlrpc.client.ServerProxy("http://rpcgame:8088") as proxy:
        proxy.restart_gameserver()

    return "gameserver restarted"


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8088)