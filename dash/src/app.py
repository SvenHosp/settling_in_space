# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

game_conn = "http://rpcgame:8082"
game_started = False

starsystemsDictStatic = {}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Settling in Space'),
    dcc.Interval(
        id='intervalComponent',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    html.Div(children=[
        html.H2(children='Main Menu'),
        html.Div('status game server', id='gameserverstatus'),

        html.Button('configure', id='configure', n_clicks=0),
        html.Button('initialize', id='initialize', n_clicks=0),
        html.Button('start', id='start', n_clicks=0),
        html.Div('status game server', id='gameserveroutput')
    ]),
    html.Div(children=[
        html.H2(children='GamePanel'),
        html.Button('show Stars', id='loadStars', n_clicks=0),

        html.Div(children='''
            Stars:
        '''),
        dcc.Dropdown(
            id='stardropdown'
        ),
        dcc.Dropdown(
            id='planetdropdown'
        ),
        html.Div('no planet selectes', id='graphstarsystem')
        
    ],
        style={'width': '600px', 'display': 'inline-block'}
    )
])


@app.callback(dash.dependencies.Output('gameserverstatus', 'children'),
              [dash.dependencies.Input('intervalComponent', 'n_intervals')])
def update_gamestatus(n):
    global game_started
    try:
        import xmlrpc.client
        
        with xmlrpc.client.ServerProxy(game_conn) as proxy:
            runningState = proxy.getRunningStats()
            status = proxy.getGameStatus()
            
            if runningState == status:
                game_started = True
            else:
                game_started = False
            
            return status
    except:
        game_started = False
        return 'no connection possible'

@app.callback(dash.dependencies.Output('stardropdown', 'options'),
              [dash.dependencies.Input('loadStars', 'n_clicks')])
def update_stars_dropdown(n):
    try:
        import xmlrpc.client
        global starsystemsDictStatic

        stars_list = {}
        with xmlrpc.client.ServerProxy(game_conn) as proxy:
            starsystemsDictStatic = proxy.getStarSystemsDictStatic()

        return [{'label': i, 'value': i} for i in list(starsystemsDictStatic.keys())]
    except:
        return [{'label': "game not started yet.", 'value': '<empty>'}]

@app.callback(dash.dependencies.Output('planetdropdown', 'options'),
              [dash.dependencies.Input('stardropdown', 'value')])
def update_planets_dropdown(sel_value):
    try:
        return [{'label': i, 'value': i} for i in starsystemsDictStatic[sel_value]]
    except:
        return [{'label': "No star selected.", 'value': '<empty>'}]


@app.callback(dash.dependencies.Output('graphstarsystem', 'children'),
              [dash.dependencies.Input('stardropdown', 'value')])
def show_star_graph(sel_value):
    try:
        import xmlrpc.client
        import pandas as pd
        
        with xmlrpc.client.ServerProxy(game_conn) as proxy:
            star_obj_list = proxy.getStarSystemObjectsAsList(sel_value)
            df = pd.DataFrame(star_obj_list, columns =['x', 'y', 'z', 'name'])
            fig = px.scatter_3d(df, x='x', y='y', z='z',
              color='name')
            graph = dcc.Graph(figure=fig)
            
            return graph
    except:
        return ''


@app.callback(
    dash.dependencies.Output('gameserveroutput', 'children'),
    [dash.dependencies.Input('configure', 'n_clicks'),
     dash.dependencies.Input('initialize', 'n_clicks'),
     dash.dependencies.Input('start', 'n_clicks')])
def manage_gameserver(btn1, btn2, btn3):
    import xmlrpc.client
    msg = ''
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    try:
        if 'configure' in changed_id:
            with xmlrpc.client.ServerProxy(game_conn) as proxy:
                proxy.configure()
            msg = 'game configured (default)'
        elif 'initialize' in changed_id:
            with xmlrpc.client.ServerProxy(game_conn) as proxy:
                proxy.initialize()
            msg = 'game initialized and is now ready'
        elif 'start' in changed_id:
            with xmlrpc.client.ServerProxy(game_conn) as proxy:
                proxy.start()
            msg = 'game started'
    except:
        pass
    finally:
        return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')