import dash
from dash import html

app = dash.Dash(__name__)

server = app.server



app.layout = html.Div("HI amgad!")


app.run()