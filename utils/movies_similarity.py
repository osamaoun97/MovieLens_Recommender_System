import pandas as pd
from sklearn.metrics.pairwise import (cosine_similarity, euclidean_distances, manhattan_distances)
from sklearn.metrics import pairwise_distances
import numpy as np

class MoviesSimilarity:
    def __init__(self):
        # Load the ratings data from the merged_ratings.csv file
        self.data = pd.read_csv("data/merged_ratings.csv")
        self.movies = self.data[["movie_title", 'movieId']].drop_duplicates()
                
    def create_similarity_matrix(self, similarity_type='cosine'):
        # Pivot the data to create a user-item matrix
        utility_matrix = self.data.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)

        # Compute the similarity matrix based on the given similarity type
        if similarity_type == 'cosine':
            similarity_matrix = cosine_similarity(utility_matrix)  # Compute cosine similarity between items
        elif similarity_type == 'euclidean':
            similarity_matrix = 1 / (1 + euclidean_distances(utility_matrix))  # Compute Euclidean distance similarity
        elif similarity_type == 'manhattan':
            similarity_matrix = 1 / (1 + manhattan_distances(utility_matrix))  # Compute Manhattan distance similarity
        elif similarity_type == 'adjusted_cosine':
            centered_matrix = utility_matrix.subtract(utility_matrix.mean(axis=1), axis=0)
            similarity_matrix = 1 - pairwise_distances(centered_matrix, metric='cosine')  # Compute adjusted cosine similarity
        elif similarity_type == 'pearson':
            centered_matrix = utility_matrix.subtract(utility_matrix.mean(axis=1), axis=0)
            similarity_matrix = 1 - pairwise_distances(centered_matrix, metric='correlation')  # Compute Pearson correlation similarity
        elif similarity_type == 'mean_squared_diff':
            similarity_matrix = np.exp(-pairwise_distances(utility_matrix, metric='sqeuclidean'))  # Compute mean squared difference similarity
        else:
            raise ValueError(f"Invalid similarity_type: {similarity_type}")
        
        similarity_matrix = pd.DataFrame(similarity_matrix, index=utility_matrix.index, columns=utility_matrix.index)
        
        return similarity_matrix
        
    def get_most_similar_items(self, item_title, similarity_type='cosine', top_n=5):
        
        # Create the similarity matrix
        similarity_matrix = self.create_similarity_matrix(similarity_type)

        # Find the index of the item in the data
        item_index = self.movies.loc[self.movies['movie_title'] == item_title, "movieId"].values[0]
        
        # Get the similarity scores for the item
        item_similarities = similarity_matrix[similarity_matrix.index == item_index].values[0]

        # Sort the similarities in descending order and get the indices of the most similar items
        most_similar_indices = item_similarities.argsort()[::-1][1:top_n + 1]
        
        # Get the titles of the most similar items
        most_similar_items = self.movies.iloc[most_similar_indices, :]["movie_title"].tolist()
        
        return most_similar_items

    
if __name__ == "__main__":
    similarity = MoviesSimilarity()

    # Specify the movie name for which you want to find similar items
    movie_name = "Toy Story (1995)"

    # Get similar items based on different similarity measures
    similar_items_cosine = similarity.get_most_similar_items(movie_name, similarity_type='cosine', top_n=5)
    similar_items_euclidean = similarity.get_most_similar_items(movie_name, similarity_type='euclidean', top_n=5)
    similar_items_manhattan = similarity.get_most_similar_items(movie_name, similarity_type='manhattan', top_n=5)
    similar_items_adjusted_cosine = similarity.get_most_similar_items(movie_name, similarity_type='adjusted_cosine', top_n=5)
    similar_items_pearson = similarity.get_most_similar_items(movie_name, similarity_type='pearson', top_n=5)
    similar_items_mean_squared_diff = similarity.get_most_similar_items(movie_name, similarity_type='mean_squared_diff', top_n=5)

    # Print the results
    print("Similar items based on cosine similarity:", similar_items_cosine)
    print("Similar items based on Euclidean distance similarity:", similar_items_euclidean)
    print("Similar items based on Manhattan distance similarity:", similar_items_manhattan)
    print("Similar items based on adjusted cosine similarity:", similar_items_adjusted_cosine)
    print("Similar items based on Pearson correlation coefficient:", similar_items_pearson)
    print("Similar items based on mean squared difference similarity:", similar_items_mean_squared_diff)
