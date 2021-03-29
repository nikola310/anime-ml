import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import seaborn as sns

from anime import preprocess_data
from pandas import Series
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

if __name__ == "__main__":
    anime_data = pd.read_csv("data/anime_cleaned.csv", sep=',')
    anime_data, anime_features = preprocess_data(anime_data, verbose=False)

    print('Mean score of all anime in the data:', anime_data.score.mean())
    print('Median of anime score:', anime_data.score.median())

    print('Mean number of episodes:', anime_data.episodes.mean())
    print('Median number of episodes:', anime_data.episodes.median())

    print(anime_data)

    print('Mean number of minutes per episodes:', anime_data.duration_min.mean())
    print('Median number of minutes per episodes:', anime_data.duration_min.median())

    most_popular_anime = anime_data.loc[anime_data.members.idxmax()]
    print('Most popular anime', most_popular_anime.title, 'with', int(most_popular_anime.members), 'members on MAL')