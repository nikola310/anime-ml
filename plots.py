import pandas as pd
import numpy as np
import unicodedata
import seaborn as sns
import matplotlib.pyplot as plt
from anime import preprocess_data
from pandas import Series

location_data = pd.read_csv("data/clean-locations.csv", sep=',')
anime_data = pd.read_csv("data/anime_cleaned.csv", sep=',')
anime_data, anime_features = preprocess_data(anime_data, verbose=False)

#sns.pairplot(anime_data)

anime_data['source'].value_counts().plot(kind='bar')
plt.savefig('source.png', bbox_inches='tight')

anime_data['type'].value_counts().plot(kind='bar')
plt.savefig('type.png', bbox_inches='tight')