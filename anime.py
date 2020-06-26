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

def preprocess_data(anime, verbose=True):

	if verbose:
		print('Dataset before preprocessing')
		print(anime.head())

	anime['name'].str.replace('&#039;', '\'', regex=False)

	anime.loc[(anime['type'] == 'OVA') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
	anime.loc[(anime['genre'] == 'Hentai') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
	anime.loc[(anime['type'] == 'Movie') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'

	known_anime_episodes = {'Naruto: Shippuuden': 500, 'One Piece': 784, 'Detective Conan': 854, 
							'Dragon Ball Super': 86, 'Crayon Shin-chan': 942, 'Yu☆Gi☆Oh! Arc-V': 148,
							'Shingeki no Kyojin Season 2': 25, 'Boku no Hero Academia 2nd Season': 25,
							'Little Witch Academia (TV)': 25}

	if verbose:
		print_known_animes_and_current_episodes(known_anime_episodes, anime)

	for k, v in known_anime_episodes.items():
		anime.loc[anime['name'] == k, 'episodes'] = v

	if verbose:
		print_known_animes_and_current_episodes(known_anime_episodes, anime)

	anime['episodes'] = anime['episodes'].map(lambda x: np.nan if x == 'Unknown' else x)
	anime['episodes'].fillna(anime['episodes'].median(), inplace = True)

	dummies = pd.get_dummies(anime[['type']])

	anime['rating'] = anime['rating'].astype(float)
	anime['rating'].fillna(anime['rating'].median(), inplace = True)
	anime['members'] = anime['members'].astype(float)

	anime.dropna(subset=['anime_id'], inplace=True)
	
	anime['anime_id'] = anime['anime_id'].astype(int)
	# Scaling
	anime['genre'] = anime['genre'].str.replace(" ", "")
	anime_features = pd.concat([anime['genre'].str.get_dummies(sep=','),
								pd.get_dummies(anime[['type']]),
								anime[['rating']], anime[['members']], anime['episodes']], axis=1)

	if verbose:
		print('==================Anime features==================')
		print(anime_features.head())
		print(anime_features.columns)

	min_max_scaler = MinMaxScaler()
	anime_features = min_max_scaler.fit_transform(anime_features)

	if verbose:
		print('==================Anime features after scaling==================')
		print(np.round(anime_features, 2))

	if verbose:
		print('Dataset after preprocessing')
		print(anime.head())

	return (anime, anime_features)

def get_index_from_name(anime, name):
	return anime[anime['name'] == name].index.tolist()[0]

def get_index_from_partial_name(anime, partial_name):
	for name in list(anime.name.values):
		if partial_name in name:
			print(name, get_index_from_name(anime, name))

def print_similar_animes(indices, anime, query=None, id=None):
	if id:
		for id in indices[id][1:]:
			print(anime.loc[id]['name'])
	if query:
		found_id = get_index_from_name(anime, query)
		for id in indices[found_id][1:]:
			print(anime.loc[id]['name'])

def train_knn_model(anime_data, anime_features):
	nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(anime_features)
	print('Start training')
	distances, indices = nbrs.kneighbors(anime_features)
	print('Training finished')
	return distances, indices


if __name__ == '__main__':
	anime_data = pd.read_csv("data/anime.csv", sep=',')
	anime_data, anime_features = preprocess_data(anime_data, verbose=False)
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
	print_similar_animes(indices, anime_data, id=719)
	print('==========================================================')
	print('Animes similar to Koutetsujou no Kabaneri')
	print_similar_animes(indices, anime_data, id=1976)

