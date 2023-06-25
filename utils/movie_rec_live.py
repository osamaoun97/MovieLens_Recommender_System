import tensorflow as tf
import tensorflow_recommenders as tfrs
import pandas as pd
class MovieRecommender:
    def __init__(self):
        self.movie_model = tf.keras.models.load_model('models/multitask_model').movie_model
        self.movie_recommender = tfrs.layers.factorized_top_k.BruteForce(self.movie_model, k=100)
        mv = pd.Series(self.movie_model.get_layer('movies_lookup').get_vocabulary())
        movie_dataset = tf.data.Dataset.from_tensor_slices(mv.unique())
        self.movie_recommender.index_from_dataset(movie_dataset.batch(100).map(lambda title: (title, self.movie_model(title))))
    
    def get_recommendations(self, movie_name, n):
        movie_name = tf.constant([movie_name])
        scores, recommended_items = self.movie_recommender(movie_name)
        return [item.decode('utf-8') for item in recommended_items.numpy()[0].tolist() if item.decode('utf-8') != movie_name]

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
    
    
    # from movies_similarity import MoviesSimilarity
    # movies = list(MoviesSimilarity().movies["movie_title"])
    
    # recommender = MovieRecommender()
    # recommendations = []
    # for movie in movies:
    #     movies_recommendations = recommender.get_recommendations(movie, 50)
    #     recommendations.append(movies_recommendations)

    # df = pd.DataFrame(recommendations, index=movies)
    # df.to_csv('data/movies_recommendations.csv')
    