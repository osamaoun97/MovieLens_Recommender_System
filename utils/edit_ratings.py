import pandas as pd

# Read the first CSV file
movies_df = pd.read_csv('data/movies.csv')

# Read the second CSV file
ratings_df = pd.read_csv('data/ratings.csv')

# Merge the two dataframes based on the movieId column
merged_df = pd.merge(ratings_df, movies_df[['movieId', 'title']], on='movieId', how='left')

# Rename the movieId column to title
merged_df.rename(columns={'title': 'movie_title'}, inplace=True)

# remove uneeded columns
merged_df.drop(["timestamp"], axis=1, inplace=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('data/merged_ratings.csv', index=False)
