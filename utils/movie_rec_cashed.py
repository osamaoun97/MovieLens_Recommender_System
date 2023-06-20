import pandas as pd

class MovieRecommender:
    def __init__(self):
        self.recommendations_df = pd.read_csv('data/movies_recommendations.csv', index_col=0)
    
    def get_recommendations(self, movie_name, n):
        movies_recommendations = self.recommendations_df.loc[movie_name].tolist()[:n]
        return movies_recommendations

if __name__ == '__main__':
    # Path to the pre-trained model
    # Create an instance of the Recommender class
    rec = MovieRecommender()
    # Movie Name for which to get recommendations
    movie_name = "Grumpier Old Men (1995)"
    # Get recommendations
    predictions = rec.get_recommendations(movie_name, 10)
    # Print the predictions
    print(predictions)
    