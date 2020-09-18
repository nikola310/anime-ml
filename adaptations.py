import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
import json

data_to_drop = ['title_synonyms', 'title_japanese', 'title_english', 'image_url', 'status', 'airing', 
				'aired_string', 'background', 'broadcast', 'producer', 'licensor', 'opening_theme',
				'ending_theme', 'duration', 'aired', 'premiered', 'studio']

def preprocess_data(anime, verbose=True):

	if verbose:
		print('Dataset before preprocessing')
		print(anime.head())

	anime['title'] = anime['title'].str.replace('&#039;', '\'', regex=False)

	anime.loc[(anime['type'] == 'OVA') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
	anime.loc[(anime['genre'] == 'Hentai') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'
	anime.loc[(anime['type'] == 'Movie') & (anime['episodes'] == 'Unknown'), 'episodes'] = '1'

	# Drop unnecesary data
	for column in data_to_drop:
		anime.drop(column, 1, inplace=True)

	anime = anime.drop(anime[anime.score == 0].index)
	anime = anime.drop(anime[anime.related.isna()].index)
	
	anime['related'] = anime['related'].str.replace('\"', '')
	anime['related'] = anime['related'].str.replace('\'', '\"')

	if verbose:
		print('Dataset after preprocessing')
		print(anime.head())

	return anime

def get_json_object(json_string):
	#TODO change to get ids, not urls
	json_data = json.loads(json_string)
	ids = []
	if isinstance(json_data, dict):
		for key in json_data.keys():
			
			for related in json_data[key]:
				try:
					if related['type'] == 'manga':
						
						ids.append(related['mal_id'])
				except:
					continue
	else:
		for value in json_data:
			try:
				if related['type'] == 'manga':
					
					ids.append(related['ids'])
			except:
				continue
	if not ids:
		ids = np.nan
	#if len(ids) > 1:
	#	print(type(ids))
	return ids

def extract_related_manga_links(anime):
	manga_ids = anime['related'].apply(get_json_object)
	return manga_ids

if __name__ == '__main__':
	anime_data = pd.read_csv("data/anime_cleaned.csv", sep=',')
	anime_data = preprocess_data(anime_data, verbose=False)
	anime_data['manga_ids'] = extract_related_manga_links(anime_data)

	anime_data.dropna(subset=['manga_ids'], inplace=True)

	anime_data.to_csv(path_or_buf='data/manga_ids.tsv', sep='\t', columns=['anime_id', 'manga_ids'], index=False)