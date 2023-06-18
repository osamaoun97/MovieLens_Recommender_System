class MovieData:
  def __init__(self, data, rating_threshold, count_threshold):
    self.rating_threshold = rating_threshold
    self.count_threshold = count_threshold
    self.data = data

  def get_highest_rated(self, n=20):
    # Return top n rated movies rated at least self.count_threhold times
    ratings_count = self.data.groupby(['movieTitle'])['rating'].count()
    popular_movies = ratings_count[ratings_count>self.count_threshold].index
    highest_rated_movies = self.data[self.data['movieTitle'].isin(popular_movies)].groupby('movieTitle').mean('rating')['rating'].sort_values(ascending=False)[:n]
    return highest_rated_movies

  def get_most_rated(self, n=20):
    # Return top n most rated movies with average rating more than self.rating_threhold times
    average_rating = self.data.groupby(['movieTitle'])['rating'].mean('rating')
    popular_movies = average_rating[average_rating>self.rating_threshold].index
    most_rated_movies = self.data[self.data['movieTitle'].isin(popular_movies)].groupby('movieTitle').count()['userId'].sort_values(ascending=False)[:n]
    return most_rated_movies