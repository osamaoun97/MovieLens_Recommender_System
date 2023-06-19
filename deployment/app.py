import dash
from dash import  dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from utils.user_rec import UserRecommender
import deployment.themes as themes

print("loading model")
UserRecommender = UserRecommender()
print("model loaded")

users = list(range(1,944))

app = dash.Dash(__name__, external_stylesheets=[themes.SKETCHY])

server = app.server

app.layout = html.Div([
    html.H1("Recommendation App"),
    html.Div([
        html.Label("User ID:"),
        dcc.Dropdown(
            id='input-user-id',
            options=[{'label': user_id, 'value': user_id} for user_id in users],
            placeholder='Select a user ID'
        ),
    ]),
    html.Div([
        html.Label("Number of recommended items:"),
        dcc.Input(
            id='input-num-items',
            type='number',
            placeholder='Enter number of items'
        ),
    ]),
    dbc.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-recommendations')
])

@app.callback(
    Output('output-recommendations', 'children'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('input-user-id', 'value'),
     dash.dependencies.State('input-num-items', 'value')]
)
def update_recommendations(n_clicks, user_id, num_items):
    
        recommended_items = UserRecommender.get_recommendations(str(user_id))[:num_items]
        return html.Ul([html.Li(item) for item in recommended_items])

app.run()