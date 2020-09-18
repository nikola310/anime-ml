import pickle
import re
import requests
import json
import csv
import sys
import pandas as pd
from pandas import DataFrame
import ast
import os.path

base_url = "http://api.jikan.moe/v3/manga/"
attributes_to_drop = ['request_hash', 'request_cached', 'request_cache_expiry']
csv_keys = ['mal_id', 'url', 'title', 'title_english', 'title_synonyms', 'title_japanese', 'status', 'image_url',
			'type', 'volumes', 'chapters', 'publishing', 'published', 'rank', 'score', 'scored_by', 'popularity',
			'members', 'favorites', 'synopsis', 'background', 'related', 'genres', 'authors', 'serializations']

def trim_newlines(jsonData):
	if jsonData['background']:
		jsonData['background'] = jsonData['background'].replace('\n', '')
		jsonData['synopsis'] = jsonData['synopsis'].replace('\n', '')

	return jsonData


def get_manga(row, csv_writer, scraped_mangas):
	id_list = ast.literal_eval(row['manga_ids'])

	for i in id_list:
		
		if scraped_mangas is not None:
			if (scraped_mangas['mal_id'] == i).any():
				print('Manga with id {} already exists in file, moving on'.format(i))
				continue

		print('No manga  with id', i)
		page = requests.get(base_url + str(i), headers={'Content-type': 'text/plain; charset=utf-8'})
		retry_attempts = 0
		while retry_attempts < 5 and page.status_code != 200:
			if page.status_code == 404:
				print('Page with id {} doesn\'t exist, moving on.'.format(i))
				print(page.content)
				break

			retry_attempts += 1
			print('Response not correct, retrying...')
			page = requests.get(base_url + str(i))
		if page.status_code != 200:
			print('Bruh moment with code {} at manga {}'.format(page.status_code, i))
			break

		c = page.content

		jsonData = json.loads(c)

		for attr in attributes_to_drop:
			del jsonData[attr]
		
		if jsonData:
			csv_writer.writerow(jsonData)
			
	return -1

if __name__ == "__main__":

	manga_ids = pd.read_csv('data/manga_ids.tsv', sep='\t')
	
	file_object = None
	file_object = open('data/mangas.csv', 'a')

	if file_object is None:
		print('Bruh moment, destination file is None')
		sys.exit(1)
	
	scraped_mangas = None
	csv_writer = csv.DictWriter(file_object, csv_keys)
	if os.stat('data/mangas.csv').st_size == 0:
		csv_writer.writeheader()
	else:
		scraped_mangas = pd.read_csv('data/mangas.csv')
		print('New file, adding header.')

	manga_ids.apply(get_manga, args=[csv_writer, scraped_mangas], axis=1)

	print('Scraping completed')
