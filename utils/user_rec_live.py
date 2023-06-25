import tensorflow as tf
import pandas as pd

class UserRecommender:
    """A class that provides movie recommendations for a given user."""
    def __init__(self):
        """Initializes the recommender by loading the pre-trained model and movie titles."""
        #self.model = tf.keras.models.load_model('models/explicit_model')
        self.model = tf.keras.models.load_model('models/multitask_model')
        #self.movies = pd.read_csv('data/movies.csv')['title'].unique()
        self.ratings = pd.read_csv("data/merged_ratings.csv")
        self.user_ids = self.model.get_layer('user_model').get_layer('users_lookup').get_vocabulary()
        self.movie_titles = self.model.get_layer('movie_model').get_layer('movies_lookup').get_vocabulary()
        self.num_movies = len(self.movie_titles)
    def get_recommendations(self, user_id):
        """Generate movie recommendations for a given user ID.
        Args:
          - user_id (str): The id of the user. It should be a string like "42"
          
        Returns: List of ranked movies recommendation e.g. ['Godfather', 'Godfather2']
        """
        assert str(user_id) in self.user_ids    # User not in train set!
        model_input = {"userId": tf.tile([str(user_id)], [self.num_movies]), "movieTitle": self.movie_titles}
        user_embeddings, movie_embeddings, predicted_ratings = self.model(model_input)
        recommended_items = tf.gather(self.movie_titles, tf.squeeze(tf.argsort(predicted_ratings, axis=0, direction='DESCENDING')))
        recommended_items = [item.decode('utf-8') for item in recommended_items.numpy()]
        rated_items = self.ratings[self.ratings["userId"] == user_id]["movie_title"].tolist()
        final_recommendations =[x for x in recommended_items if x not in rated_items][:50]
        return final_recommendations #, rated_items # Not sure what you wanted to return here?
    
if __name__ == '__main__':
    import sys
    import pandas as pd
    users = pd.read_csv('data/ratings.csv').sort_values('userId')['userId'].unique().tolist()

    recommender = UserRecommender()
    recommendations = []
    for user_id in users:
        user_recommendations = recommender.get_recommendations(user_id)
        recommendations.append(user_recommendations[:50])

    df = pd.DataFrame(recommendations, index=users)
    #print(df.head(5))
    
    df.to_csv('data/user_recommendations.csv', index_label='User ID')
    #recommender = UserRecommender()
    # if len(sys.argv) > 1:
    #   inputs = sys.argv[1:]
    #   for user in inputs:
    #     user_id = int(user)  # Example user ID
        
    #     recommendations, rated = recommender.get_recommendations(user_id)
    #     print("recommendations:", recommendations)
    #     print("Rated:", rated)
    # else:
    #   user_id = 1  # Example user ID
    #   recommendations, rated = recommender.get_recommendations(user_id)
    #   print("recommendations:", recommendations)
    #   print("Rated:", rated)
