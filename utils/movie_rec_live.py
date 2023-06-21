import tensorflow as tf

class MovieRecommender:
    def __init__(self):
        self.model = tf.keras.models.load_model('models/movie_model')
    
    def get_recommendations(self, movie_name, n):
        movie_name = tf.constant([movie_name])
        recommended_items = self.model(movie_name)
        return [item.decode('utf-8') for item in recommended_items[1].numpy()[0].tolist()][1:n+1]

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
    