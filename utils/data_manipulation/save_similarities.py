import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances, pairwise_distances
import numpy as np

class SimilarityMatrixSaver:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)

    def save_similarity_matrix(self, similarity_type, output_file):
        # Pivot the data to create a user-item matrix
        matrix = self.data.pivot_table(index='movieId', columns='userId', values='rating').fillna(0)

        # Compute the similarity matrix based on the given similarity type
        if similarity_type == 'cosine':
            similarity_matrix = cosine_similarity(matrix)
        elif similarity_type == 'euclidean':
            similarity_matrix = 1 / (1 + euclidean_distances(matrix))
        elif similarity_type == 'manhattan':
            similarity_matrix = 1 / (1 + manhattan_distances(matrix))
        elif similarity_type == 'adjusted_cosine':
            centered_matrix = matrix.subtract(matrix.mean(axis=1), axis=0)
            similarity_matrix = 1 - pairwise_distances(centered_matrix, metric='cosine')
        elif similarity_type == 'pearson':
            centered_matrix = matrix.subtract(matrix.mean(axis=1), axis=0)
            similarity_matrix = 1 - pairwise_distances(centered_matrix, metric='correlation')
        elif similarity_type == 'mean_squared_diff':
            similarity_matrix = np.exp(-pairwise_distances(matrix, metric='sqeuclidean'))
        else:
            raise ValueError("Invalid similarity type.")

        # Convert the similarity matrix to a DataFrame
        similarity_df = pd.DataFrame(similarity_matrix, index=matrix.index, columns=matrix.index)

        # Save the similarity matrix as a CSV file
        similarity_df.to_csv(output_file)

# Example usage
saver = SimilarityMatrixSaver("data/merged_ratings.csv")
saver.save_similarity_matrix('cosine', 'data/similarities/similarity_cosine.csv')
saver.save_similarity_matrix('euclidean', 'data/similarities/similarity_euclidean.csv')
saver.save_similarity_matrix('manhattan', 'data/similarities/similarity_manhattan.csv')
saver.save_similarity_matrix('adjusted_cosine', 'data/similarities/similarity_adjusted_cosine.csv')
saver.save_similarity_matrix('pearson', 'data/similarities/similarity_pearson.csv')
saver.save_similarity_matrix('mean_squared_diff', 'data/similarities/similarity_mean_squared_diff.csv')
