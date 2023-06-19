from datetime import datetime
import dash
from dash import  dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from utils.user_rec_cashed import UserRecommenderCashed
from utils.general_rec import GeneralRecommender
from utils.movies_similarity_saved import MoviesSimilarity
from utils.graphs import PlotlyGraphs

pg = PlotlyGraphs()

ur = UserRecommenderCashed()
users = list(range(1, 944))

gr = GeneralRecommender(rating_threshold=3, count_threshold=50)

ms = MoviesSimilarity()
movies = list(MoviesSimilarity().movies["movie_title"])

similarity_measures = ["cosine", "adjusted_cosine", "euclidean", "manhattan", "pearson", "mean_squared_diff"]
highest_rated = gr.get_highest_rated(n=10)
most_rated = gr.get_most_rated(n=10)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

server = app.server


tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.Br(),
            html.H5("Welcome to our recommender app! 👋 if you are a new users, here are some recommendations for you ✨:", className="card-text"),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(dbc.Card([
                    html.H6("Higest rated movies 🔝", style={'font-size': '25px', "display": "flex", "justify-content": "center", "align-items": "center", "color": "#66b2b2"}),
                    html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(highest_rated, start=1)],style={'font-size': '15px'})
            ])),
                dbc.Col(dbc.Card([
                    html.H6("Most Popular movies 📈", style={'font-size': '25px', "display": "flex", "justify-content": "center", "align-items": "center", "color": "#66b2b2"}),
                    html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(most_rated, start=1)],style={'font-size': '15px'})
            ]))
            ]),
            html.Br(),
            html.Br(),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
        html.H5("Already a user 👤? Select your ID and see what is recommended for you:", className="card-text"),
        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card([
                html.Label("User ID:"),
                dcc.Dropdown(
                id="input-user-id",
                options=users,
                placeholder="Select an ID",
                style={"color": "#000000","background-color": "#cccccc"}
                ),])),
            dbc.Col(dbc.Card([
                html.Label("Number of Recommendations:"),
                dcc.Slider(
                id="input-num-movies",
                min=0,
                max=20,
                step=2,
                value=10,
                marks={i: str(i) for i in range(0, 21, 2)},
                ),])),
            ]),
        html.Br(),
        dbc.Button("Submit", id="users-movies-button", n_clicks=0),
        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card([
            html.H6("Recommended movies ", style={'font-size': '25px', "display": "flex", "justify-content": "center", "align-items": "center", "color": "#66b2b2"}),
            html.Ul(style={'font-size': '15px'}, id="users-movies-rec")
            ])),
            ]),
        ]
        ),
    className="mt-3",
)

tab3_content = dbc.Card(
    dbc.CardBody(
        [
        html.H5("Did you like a movie 🎬 and want a similar one? use our similarity measures 📏:", className="card-text"),
        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card([
                html.Label("Movie Name:"),
                dcc.Dropdown(
                id="input-movie",
                options=movies,
                placeholder="Select a movie",
                style={"color": "#000000","background-color": "#cccccc"}
                ),])),
            dbc.Col(dbc.Card([
                html.Label("Similarity Measure:"),
                dcc.Dropdown(
                id="sim_measure",
                options=similarity_measures,
                placeholder="Select a similarity measure",
                style={"color": "#000000","background-color": "#cccccc"}
                ),])),
            ]),
        html.Br(),
        dbc.Button("Submit", id="movies-sim-button", n_clicks=0),
        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card([
            html.H6("Top similar movies", style={'font-size': '25px', "display": "flex", "justify-content": "center", "align-items": "center", "color": "#66b2b2"}),
            html.Ul(style={'font-size': '15px'}, id="movies-sim-rec")
            ])),
            ]),
        ]
        ),
    className="mt-3",
)

PANS = dbc.Row([    
    dbc.Col([
        dbc.Card(
        [
            dbc.CardImg(src="/assets/Users.png",style={'height':'2%','width':'25%','padding-top':'3px'},className = 'align-self-center', top=True),
            dbc.CardBody([
                html.H6("Number of Users", className="card-text",style={'font-size': '15px', "font-weight": "bold"}),
                html.H1("943", style={'font-size': '20px', "font-weight": "bold"})
            ])
        ],
        style={"width": "26rem",'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.2)','border-radius': '5px'},
    )
    ],width=4, style={"height": "170px", "background-color": "transparent", 'text-align':'center'}),

    dbc.Col([
        dbc.Card(
        [
            dbc.CardImg(src="/assets/MovieS.png",style={'height':'2%','width':'25%','padding-top':'3px'},className = 'align-self-center', top=True),
            dbc.CardBody([
                html.H6("Number of Movies", className="card-text",style={'font-size': '15px', "font-weight": "bold"}),
                html.H1("9743", style={'font-size': '20px', "font-weight": "bold"})
            ])
        ],
        style={"width": "26rem",'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.2)','border-radius': '5px'},
    )
    ],width=4, style={"height": "170px", "background-color": "transparent", 'text-align':'center'}),

        dbc.Col([
        dbc.Card(
        [
            dbc.CardImg(src="/assets/Ratings.png",style={'height':'2%','width':'25%','padding-top':'3px'},className = 'align-self-center', top=True),
            dbc.CardBody([
                html.H6("Number of Ratings", className="card-text",style={'font-size': '15px', "font-weight": "bold"}),
                html.H1('100837', style={'font-size': '20px', "font-weight": "bold"})
            ])
        ],
        style={"width": "26rem",'box-shadow': '0 4px 4px 0 rgba(0,0,0,0.2)','border-radius': '5px'},
    )
    ],width=4, style={"height": "170px", "background-color": "transparent", 'text-align':'center'}),
])

GRAPHS = tab6_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=pg.dist_of_ratings()),
                    width=6),
            dbc.Col(dcc.Graph(figure=pg.count_by_genre()),
                    width=6)
        ],style={"height": "380px"})
    ]),
    className="mt-3",
)

tab4_content = dbc.Card(
    dbc.CardBody(
        [
            PANS,
            html.Br(),
            GRAPHS,
        ]
        ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Main page", label_style={"color": "#b2d8d8"}),
        dbc.Tab(tab2_content, label="Users Recommendation", label_style={"color": "#b2d8d8"}),
        dbc.Tab(tab3_content, label="Movies Similarity", label_style={"color": "#b2d8d8"}),
        dbc.Tab(tab4_content, label="Data Statistics", label_style={"color": "#b2d8d8"}),
    ]
)
header = dbc.Card(
    style={"display": "flex", "justify-content": "center", "align-items": "center", "color": "#b2d8d8"},
    children=[
        html.H1("Movies Recommendation App")
    ]
)

footer = html.Div([
    html.Small(f'© {datetime.now().year}. Created by: '),
    html.A('Osama Fayez', href='https://www.linkedin.com/in/osama-oun/', target='_blank', style={"color": "#008080"}),
    ', ', html.A('Amgad Hassan', href='https://www.linkedin.com/in/amgad-hasan/', target='_blank', style={"color": "#008080"}),
    ' and ', html.A('Israa Okil', href='https://www.linkedin.com/in/israa-okil/', target='_blank', style={"color": "#008080"}),
    ],id='footer', style={"text-align": "center"})

app.layout = dbc.Container([html.Br(),
                            header,
                            html.Br(),
                            tabs,
                            footer])


@app.callback(
    Output("users-movies-rec", "children"),
    [
        Input("users-movies-button", "n_clicks"),
    ],
    [
        dash.dependencies.State("input-user-id", "value"),
        dash.dependencies.State("input-num-movies", "value"),
    ],
)
def update_recommendations(n_clicks, user_id, num_items):
    if user_id and num_items:
        recommended_items = ur.get_recommendations(user_id)
        if num_items <= 10:
            return html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(recommended_items[:num_items], start=1)])
        elif num_items > 10:
            return dbc.Row([dbc.Col(html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(recommended_items[:10], start=1)])),
                            dbc.Col(html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(recommended_items[10:num_items], start=11)]))])
    else:
        return html.H6("please select the required options")

@app.callback(
    Output("movies-sim-rec", "children"),
    [
        Input("movies-sim-button", "n_clicks"),
    ],
    [
        dash.dependencies.State("input-movie", "value"),
        dash.dependencies.State("sim_measure", "value"),
    ],
)
def update_movies_sim(n_clicks, movie_name, similarity_type):
    if movie_name and similarity_type:
        similar_movies = ms.get_most_similar_items(movie_name, similarity_type = similarity_type, top_n= 20)
        return dbc.Row([dbc.Col(html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(similar_movies[:10], start=1)])),
                        dbc.Col(html.Ul([html.P(f"{i}. {item}") for i, item in enumerate(similar_movies[10:20], start=11)]))])
    else:
        return html.H6("please select the required options")


app.run()