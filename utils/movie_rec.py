import tensorflow as tf

class MovieRecommender:
    def __init__(self):
        self.model = tf.keras.models.load_model('models/movie_model')
    
    def get_recommendations(self, movie_id, n):
        movie_id = tf.constant([movie_id])
        recommended_items = self.model(movie_id)
        return [item.decode('utf-8') for item in recommended_items[1].numpy()[0].tolist()][1:n+1]

if __name__ == '__main__':
    # Path to the pre-trained model
    # Create an instance of the Recommender class
    rec = MovieRecommender()
    # Movie ID for which to get recommendations
    movie_id = "Freaky Friday (2003)"
    # Get recommendations
    predictions = rec.get_recommendations(movie_id, 10)
    # Print the predictions
    print(predictions)