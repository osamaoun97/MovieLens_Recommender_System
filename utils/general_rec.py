import pandas as pd

class GeneralRecommender:
    # Read the data from a CSV file into a pandas DataFrame
    data = pd.read_csv("data/merged_ratings.csv")

    def __init__(self, rating_threshold, count_threshold):
        # Initialize the GeneralRecommender object with rating_threshold and count_threshold
        self.rating_threshold = rating_threshold
        self.count_threshold = count_threshold

    def get_highest_rated(self, n=5):
        # Return top n rated movies rated at least self.count_threshold times
        highest_rated_movies = (
            GeneralRecommender.data
            .groupby('movie_title')['rating']
            .agg(['count', 'mean'])
            .query("count > @self.count_threshold")
            .nlargest(n, 'mean')['mean']
        )
        return highest_rated_movies.index.tolist()

    def get_most_rated(self, n=5):
        # Return top n most rated movies with average rating more than self.rating_threshold
        most_rated_movies = (
            GeneralRecommender.data
            .groupby('movie_title')['rating']
            .agg(['count', 'mean'])
            .query("mean > @self.rating_threshold")
            .nlargest(n, 'count')['count']
        )
        return most_rated_movies.index.tolist()

if __name__ == "__main__":
    # Create an instance of GeneralRecommender
    gr = GeneralRecommender(rating_threshold=3, count_threshold=50)

    # Print the highest rated movies
    print("Highest rated:", gr.get_highest_rated())

    # Print the most rated movies
    print("Most rated:", gr.get_most_rated())