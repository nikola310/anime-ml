import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

def print_known_animes_and_current_episodes(known_anime_episodes, anime):
	
	for k in known_anime_episodes.keys():
		a = anime[anime['name'] == k]
		print(f"Anime: { a.iloc[0]['name'] }, episodes: { a.iloc[0]['episodes']}")

def get_scaled_features(anime, verbose=True):
	anime['genre'] = anime['genre'].str.replace(" ", "")
	anime_features = pd.concat([anime['genre'].str.get_dummies(sep=','),
								pd.get_dummies(anime[['type']]),
								pd.get_dummies(anime[['rating']]),
								pd.get_dummies(anime[['source']]),
								anime[['scored_by']],
								anime[['rank']],
								anime[['popularity']],
								anime[['members']], anime[['favorites']],
								anime[['duration_min']],
								anime[['aired_from_year']], anime[['score']],
								anime[['members']],
								anime[['episodes']]],
								axis=1)

	if verbose:
		print('==================Anime features==================')
		print(anime_features.head())
		print(anime_features.columns)

	min_max_scaler = MinMaxScaler()
	anime_features = min_max_scaler.fit_transform(anime_features)

	if verbose:
		print('==================Anime features after scaling==================')
		print(np.round(anime_features, 2))

def preprocess_data(anime, verbose=True):

	if verbose:
		print('Dataset before preprocessing')
		print(anime.head())

	anime['title'] = anime['title'].str.replace('&#039;', '\'', regex=False)

	anime.loc[(anime['type'] == 'OVA') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
	anime.loc[(anime['genre'] == 'Hentai') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
	anime.loc[(anime['type'] == 'Movie') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'

	# Drop unnecesary data
	anime.drop('title_synonyms', 1, inplace=True)
	anime.drop('title_japanese', 1, inplace=True)
	anime.drop('title_english', 1, inplace=True)
	anime.drop('image_url', 1, inplace=True)
	anime.drop('status', 1, inplace=True)
	anime.drop('airing', 1, inplace=True)
	anime.drop('aired_string', 1, inplace=True)
	anime.drop('background', 1, inplace=True)
	anime.drop('broadcast', 1, inplace=True)
	anime.drop('producer', 1, inplace=True)
	anime.drop('licensor', 1, inplace=True)
	anime.drop('opening_theme', 1, inplace = True)
	anime.drop('ending_theme', 1, inplace = True)
	anime.drop('duration', 1, inplace = True)
	anime.drop('related', 1, inplace = True)
	anime.drop('aired', 1, inplace = True)
	anime.drop('premiered', 1, inplace = True)
	anime.drop('studio', 1, inplace = True)

	dummies = pd.get_dummies(anime[['type']])

	anime['score'] = anime['score'].astype(float)
	anime['score'].fillna(anime['score'].median(), inplace = True)
	anime['rank'].fillna(anime['rank'].median(), inplace = True)
	anime['members'] = anime['members'].astype(float)

	anime.dropna(subset=['anime_id'], inplace=True)
	anime['anime_id'] = anime['anime_id'].astype(int)

	anime_features = get_scaled_features(anime, verbose)

	if verbose:
		print('Dataset after preprocessing')
		print(anime.head())

	return (anime, anime_features)

def get_index_from_title(anime, title):
	return anime[anime['title'] == title].index.tolist()[0]

def get_index_from_partial_title(anime, partial_title):
	for name in list(anime.title.values):
		if partial_title in title:
			print(title, get_index_from_title(anime, title))

def print_similar_animes(indices, anime, query=None, id=None):
	if id:
		for id in indices[id][1:]:
			print(anime.loc[id]['title'])
	if query:
		found_id = get_index_from_title(anime, query)
		for id in indices[found_id][1:]:
			print(anime.loc[id]['title'])

def train_knn_model(anime_data, anime_features):
	nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(anime_features)
	print('Start training')
	distances, indices = nbrs.kneighbors(anime_features)
	print('Training finished')
	return distances, indices


if __name__ == '__main__':
	anime_data = pd.read_csv("data/anime_cleaned.csv", sep=',')
	anime_data, anime_features = preprocess_data(anime_data, verbose=True)
	distances, indices = train_knn_model(anime_data, anime_features)
	print('==========================================================')
	print('Animes similar to Naruto')
	print_similar_animes(indices, anime_data, query='Naruto')
	print('==========================================================')
	print('Animes similar to Noragami')
	print_similar_animes(indices, anime_data, query='Noragami')
	print('==========================================================')
	print('Animes similar to Mushishi')
	print_similar_animes(indices, anime_data, query='Mushishi')
	print('==========================================================')
	print('Animes similar to Gintama')
	print_similar_animes(indices, anime_data, query='Gintama')
	print('==========================================================')
	print('Anime movies - Naruto')
	print_similar_animes(indices, anime_data, query='The Last: Naruto the Movie') #id=2472)
	print('==========================================================')
	print('Animes similar to Koutetsujou no Kabaneri')
	print_similar_animes(indices, anime_data, query='Koutetsujou no Kabaneri') #id=28623)

