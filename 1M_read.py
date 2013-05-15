import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('../data/ml-1m/users.dat', sep = '::', header = None, names = unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('../data/ml-1m/ratings.dat', sep = '::', header = None, names = rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('../data/ml-1m/movies.dat', sep = '::', header = None, names = mnames)

data = pd.merge(pd.merge(ratings, users), movies)
mean_ratings = data.pivot_table('rating', rows = 'title', cols = 'gender', aggfunc = 'mean')
ratings_by_title = data.groupby('title').size()

active_titles = ratings_by_title.index[ratings_by_title >= 250]
mean_ratings = mean_ratings.ix[active_titles]

top_female_ratings = mean_ratings.sort_index(by = 'F', ascending = False)
top_male_ratings = mean_ratings.sort_index(by = 'M', ascending = False)

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sort_by_diff = mean_ratings.sort_index(by = 'diff')