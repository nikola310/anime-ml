# Anime and machine learning

My personal project for using various machine learning techniques on anime related dataset.

Data used: https://www.kaggle.com/azathoth42/myanimelist

# Installation

First, create conda and activate environment with:
```bash
conda create -n anime_venv python=3.7.7

conda activate anime_venv
```

After that, you can install requirements by running:

```bash
conda install -c conda-forge --file requirements.txt
```

# Scraping mangas

Scraping mangas is done in two steps, first is to extract the related manga IDs from MyAnimeList data set by running get_adaptations.py. Next step is to run scrape_mangas.py, after which the results will be available in data/mangas.csv. Scraping is done using [Jikan API](https://github.com/jikan-me/jikan).
