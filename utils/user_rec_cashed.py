import pandas as pd
    
class UserRecommenderCashed:
    def __init__(self):
        self.recommendations_df = pd.read_csv('data/user_recommendations.csv', index_col='User ID')
    
    def get_recommendations(self, user_id):
        user_recommendations = self.recommendations_df.loc[user_id].tolist()
        return user_recommendations

if __name__ == '__main__':

    user_id = 123  # Example user ID
    recommender = UserRecommenderCashed()
    recommendations_from_csv = recommender.get_recommendations(user_id)
    print("recommendations_from_csv:", recommendations_from_csv)