from anime import preprocess_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

def plot_histograms(dataframe, column):
	dataframe[column].hist(bins=50)
	plt.show()

def plot_scatter(dataframe, labels):
	sns.jointplot(x=labels[0], y=labels[1], data=dataframe)
	plt.show()

if __name__ == '__main__':
	# samo gledamo ocene
	anime_data = pd.read_csv("data/anime.csv", sep=',')
	anime_data, anime_features = preprocess_data(anime_data, verbose=False)
	anime_ratings = pd.read_csv('data/rating.csv', sep=',')

	anime_ratings = anime_ratings[anime_ratings.rating != -1]
	anime_ratings.reset_index(drop=True, inplace=True)
	
	ratings_num = anime_ratings.groupby('anime_id')['rating'].count().reset_index(name='ratings_count')

	anime_data = anime_data.join(ratings_num.set_index('anime_id'), on='anime_id', rsuffix='rat', sort=True)
	

	plot_histograms(anime_ratings, 'rating')
	plot_histograms(ratings_num, 'ratings_count')
	plot_scatter(anime_data, ('rating', 'ratings_count'))

	to_delete_list = ratings_num[ratings_num['ratings_count'] < 10]['anime_id'].values.tolist()
	anime_ratings = anime_ratings[~anime_ratings.anime_id.isin(to_delete_list)].dropna()
	anime_matrix = anime_ratings.pivot_table(index='user_id', columns='anime_id', values='rating')
	print(anime_matrix.head())