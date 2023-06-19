import pandas as pd
import numpy as np

class MoviesSimilarity:
    def __init__(self):
        self.data = pd.read_csv("data/merged_ratings.csv")
        self.movies = self.data[["movie_title", 'movieId']].drop_duplicates()
        
    def load_similarity_matrix(self, similarity_type='cosine'):
        similarity_file = f"data/similarities/similarity_{similarity_type}.csv"
        similarity_matrix = pd.read_csv(similarity_file, index_col="movieId")
        return similarity_matrix

    def get_most_similar_items(self, item_title, similarity_type='cosine', top_n=5):
        similarity_matrix = self.load_similarity_matrix(similarity_type)
        # Find the index of the item in the data
        movie_id = self.movies.loc[self.movies['movie_title'] == item_title, "movieId"].values[0]

        movies_ids = similarity_matrix.index.to_list()

        # Get the similarity scores for the item
        movie_similarities = similarity_matrix[similarity_matrix.index == movie_id]

        # Sort the similarities in descending order and get the indices of the most similar items
        most_similar_indices = movie_similarities.values[0].argsort()[::-1][1:top_n + 1]

        # Get the movie IDs associated with the highest similarity values
        most_similar_movie_ids = [movies_ids[i] for i in most_similar_indices]
        # Get the titles of the most similar items
        most_similar_items = [self.movies[self.movies["movieId"] == i]["movie_title"].values[0] for i in most_similar_movie_ids]
        
        return most_similar_items

if __name__ == "__main__":
    similarity = MoviesSimilarity()

    # Specify the movie name for which you want to find similar items
    movie_name = "Toy Story (1995)"
    # Get similar items based on different similarity measures
    similar_items_cosine = similarity.get_most_similar_items(movie_name, similarity_type='cosine', top_n=10)
    similar_items_euclidean = similarity.get_most_similar_items(movie_name, similarity_type='euclidean', top_n=10)
    similar_items_manhattan = similarity.get_most_similar_items(movie_name, similarity_type='manhattan', top_n=10)
    similar_items_adjusted_cosine = similarity.get_most_similar_items(movie_name, similarity_type='adjusted_cosine', top_n=10)
    similar_items_pearson = similarity.get_most_similar_items(movie_name, similarity_type='pearson', top_n=10)
    similar_items_mean_squared_diff = similarity.get_most_similar_items(movie_name, similarity_type='mean_squared_diff', top_n=10)

    # Print the results
    print("Similar items based on cosine similarity:", similar_items_cosine)
    print("Similar items based on Euclidean distance similarity:", similar_items_euclidean)
    print("Similar items based on Manhattan distance similarity:", similar_items_manhattan)
    print("Similar items based on adjusted cosine similarity:", similar_items_adjusted_cosine)
    print("Similar items based on Pearson correlation coefficient:", similar_items_pearson)
    print("Similar items based on mean squared difference similarity:", similar_items_mean_squared_diff)