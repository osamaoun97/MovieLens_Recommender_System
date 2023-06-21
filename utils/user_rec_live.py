import tensorflow as tf
import pandas as pd

class UserRecommender:
    """A class that provides movie recommendations for a given user."""
    def __init__(self):
        """Initializes the recommender by loading the pre-trained model and movie titles."""
        self.model = tf.keras.models.load_model('models/explicit_model')
        self.movies = pd.read_csv('data/movies.csv')['title'].unique()
        
    def get_recommendations(self, user_id):
        """Generate movie recommendations for a given user ID.
        Args:
          - user_id (str): The id of the user. It should be a string like "42"
          
        Returns: List of ranked movies recommendation e.g. ['Godfather', 'Godfather2']
        """
        assert isinstance(user_id, str)
        model_input = {"userId": tf.tile([user_id], [9737]), "movieTitle": self.movies}
        predicted_ratings = self.model(model_input)
        recommended_items = tf.gather(self.movies, tf.squeeze(tf.argsort(predicted_ratings, axis=0, direction='DESCENDING')))
        return recommended_items.numpy()
    # TO be deleted?
    def get_recommendations_from_csv(self, user_id):
        user_recommendations = self.recommendations_df.loc[user_id].tolist()
        return user_recommendations

if __name__ == '__main__':
    # recommender = UserRecommender()
    # recommendations = []
    # for user_id in range(1, 944):
    #     user_recommendations = recommender.get_recommendations(str(user_id))
    #     recommendations.append(user_recommendations)

    # df = pd.DataFrame(recommendations, index=range(1, 944))
    # df.to_csv('data/user_recommendations.csv', index_label='User ID')
    
    user_id = 42  # Example user ID
    recommender = UserRecommender()
    recommendations = recommender.get_recommendations(user_id)
    print("recommendations:", recommendations)
