import tensorflow as tf
import pandas as pd

class UserRecommender:
    def __init__(self):
        self.model = tf.keras.models.load_model('models/explicit_model')
        self.movies = pd.read_csv('data/movies.csv')['title'].unique().reshape(-1,1)
        
    def get_recommendations(self, user_id):
        user_input = {"userId": tf.tile([["42"]], [9737, 1]), "movieTitle": self.movies}
        recommended_items = self.model(user_input)
        recommended_items = tf.gather(self.movies, tf.squeeze(tf.argsort(recommended_items, axis=0, direction='DESCENDING')))
        return [item.decode('utf-8') for item in recommended_items[1].numpy()[0].tolist()]
    
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