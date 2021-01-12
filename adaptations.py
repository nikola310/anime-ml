import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
import ast

def get_better_adaptations(row, mangas, animes, better_mangas, better_animes):
	id_list = ast.literal_eval(row['manga_ids'])

	for i in id_list:
		#print(mangas[mangas['mal_id'] == i])
		#print(animes[animes['anime_id'] == row['anime_id']])
		#print('===================================================================')
		#print(mangas[mangas['mal_id'] == i]['score'])
		#print(type(mangas[mangas['mal_id'] == i]['score'][0]))
		#print(type(ast.literal_eval(animes[animes['anime_id'] == row['anime_id']]['score'])))
		#print('===================================================================')
		#print(type(mangas[mangas['mal_id'] == i]['score'] > animes[animes['anime_id'] == row['anime_id']]['score']))
		#print(type((mangas[mangas['mal_id'] == i]['score'] < animes[animes['anime_id'] == row['anime_id']]['score']).astype('bool')))
		#print(type(mangas[mangas['mal_id'] == i]['score'][0] > animes[animes['anime_id'] == row['anime_id']]['score'][0]))
		#print(type(mangas[mangas['mal_id'] == i]['score'][0] < animes[animes['anime_id'] == row['anime_id']]['score'][0]))
		#print('===================================================================')
		print(i)
		if (mangas[mangas['mal_id'] == i]['score'][0] < animes[animes['anime_id'] == row['anime_id']]['score'][0]) == False:
			#print('it\'s false')
			better_animes += 1
		else:
			better_mangas += 1
	
	return -1


if __name__ == '__main__':
	manga_anime_ids = pd.read_csv('data/manga_ids.tsv', sep='\t')

	mangas = pd.read_csv('data/mangas.csv')
	animes = pd.read_csv("data/anime_cleaned.csv")

	animes.drop('title_synonyms', 1, inplace = True)
	animes.drop('title_japanese', 1, inplace = True)
	animes.drop('title_english', 1, inplace = True)
	animes.drop('image_url', 1, inplace = True)
	animes.drop('status', 1, inplace = True)
	animes.drop('airing', 1, inplace = True)
	animes.drop('aired_string', 1, inplace = True)
	animes.drop('background', 1, inplace = True)
	animes.drop('broadcast', 1, inplace = True)
	animes.drop('producer', 1, inplace = True)
	animes.drop('licensor', 1, inplace = True)
	animes.drop('opening_theme', 1, inplace = True)
	animes.drop('ending_theme', 1, inplace = True)
	animes.drop('duration', 1, inplace = True)
	animes.drop('related', 1, inplace = True)
	animes.drop('aired', 1, inplace = True)
	animes.drop('premiered', 1, inplace = True)
	animes.drop('studio', 1, inplace = True)
	animes.drop('genre', 1, inplace = True)
	animes.drop('duration_min', 1, inplace = True)
	animes.drop('aired_from_year', 1, inplace = True)
	animes.drop('source', 1, inplace = True)
	animes.drop('episodes', 1, inplace = True)
	animes.drop('type', 1, inplace = True)
	animes.drop('rating', 1, inplace = True)

	mangas.drop('title_synonyms', 1, inplace = True)
	mangas.drop('title_japanese', 1, inplace = True)
	mangas.drop('title_english', 1, inplace = True)
	mangas.drop('image_url', 1, inplace = True)
	mangas.drop('status', 1, inplace = True)
	mangas.drop('background', 1, inplace = True)
	mangas.drop('related', 1, inplace = True)
	mangas.drop('serializations', 1, inplace = True)
	mangas.drop('authors', 1, inplace = True)
	mangas.drop('genres', 1, inplace = True)
	mangas.drop('synopsis', 1, inplace = True)
	mangas.drop('url', 1, inplace = True)
	mangas.drop('volumes', 1, inplace = True)
	mangas.drop('chapters', 1, inplace = True)
	mangas.drop('publishing', 1, inplace = True)
	mangas.drop('published', 1, inplace = True)
	mangas.drop('type', 1, inplace = True)

	print(manga_anime_ids.head())
	print('=====================================================')
	#print(mangas.head())
	print(mangas.info())
	print('=====================================================')
	#print(animes.head())
	print(animes.info())
	better_animes_no = 0
	better_mangas_no = 0

	manga_anime_ids.apply(get_better_adaptations, args=[mangas, animes, better_animes_no, better_mangas_no], axis=1)

	print(better_animes)
	print('***********************')
	print(better_mangas)