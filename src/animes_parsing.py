

import sys
import csv
import time 
import pandas as pd
from ast import literal_eval
from shikimori_api import Shikimori


def get_genres(data):
    genres = []
    for i in data:
        genres.append(i['name'])
    return ','.join(genres)

if __name__ == '__main__':
    session = Shikimori()
    api = session.get_api()
    got, lost = 0, 0
    for i in range(1, 100000):
        animes = []
        id = []
        name = []
        russian = []
        score = []
        aired_on = []
        episodes = []
        rating = [] 
        genres = [] 
        rates = [] 
        kind = []
        try:
            got+=1
            print('animes got {}'.format(got))
            animes.append(api.animes(i).GET())
        except:
            lost+=1
            print('users lost {}'.format(lost))
        for j in animes:
            id.append(j['id'])
            name.append(j['name'])
            russian.append(j['russian'])
            score.append(j['score'])
            aired_on.append(j['aired_on'])
            rating.append(j['rating'])
            episodes.append(j['episodes'])
            genres.append(j['genres'])
            rates.append(j['rates_scores_stats'])
            kind.append(j['kind'])
        df = pd.DataFrame(zip(id, name, russian, kind, score, aired_on, episodes, genres, rates), columns = ['id', 'name', 'russian', 'kind', 'score', 'aired_on', 'episodes', 'genres', 'rates'])
        df['genres'] = df['genres'].astype(str)
        df['genres'] = df['genres'].apply(literal_eval).apply(list).apply(get_genres)
        df.to_csv('animes_full.csv', mode='a', index=False, header=False)
    sys.exit(0)
