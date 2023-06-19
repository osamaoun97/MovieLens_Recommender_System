import pandas as pd
import plotly.express as px

class PlotlyGraphs:
    def __init__(self):
        self.ratings = pd.read_csv("data/ratings.csv")
        self.movies = pd.read_csv("data/movies.csv")
        
    def dist_of_ratings(self):
        fig = px.histogram(self.ratings["rating"],
                            color_discrete_sequence=["#66b2b2"],
                            labels={
                                "value": "Rating",
                                "count": "Count"
                            })
        fig.update_layout(
            title=dict(text="Distribution of ratings", font=dict(size=20)),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
        )
        return fig
    
    def count_by_genre(self):

        self.movies["genres"] = self.movies["genres"].str.split("|")

        self.movies = self.movies.explode("genres")

        genre_counts = self.movies.groupby("genres").count().reset_index().sort_values(by="movieId",ascending=True).iloc[-10:]

        fig = px.bar(genre_counts, y="genres", x="movieId",
                     text_auto=True,
                     color_discrete_sequence=["#66b2b2"],
                    orientation='h',
                     labels={
                         "genres": "Genre",
                         "movieId": "Count"
                     })
        
        fig.update_layout(
            title=dict(text="Top 10 Movies Genres", font=dict(size=20)),
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        
        fig.update_xaxes(range=[0, 5000])
        
        fig.update_traces(textposition='outside')
        
        return fig