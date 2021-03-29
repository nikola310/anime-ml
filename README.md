# Anime and machine learning

My personal project for using various machine learning techniques on anime related dataset.

Data used: https://www.kaggle.com/azathoth42/myanimelist

# Scraping mangas

Scraping mangas is done in two steps, first is to extract the related manga IDs from MyAnimeList data set by running get_adaptations.py. Next step is to run scrape_mangas.py, after which the results will be available in data/mangas.csv. Scraping is done using [Jikan API](https://github.com/jikan-me/jikan).

#TODO
comparison of ratings: anime vs manga (in other words og vs adaptation)

#TODO
check out https://github.com/deeppomf/DeepLearningAnimePapers for something interesting