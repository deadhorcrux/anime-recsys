

import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

class I2I_Recs():
    
    def __init__(self):
        df = pd.read_csv('./anime_prep.csv')
        df = df.drop(['Unnamed: 0'], axis=1)
        self.__df = df
        self.__sim_matrix = None

    def oh(self, gmap, d):
        ans = []
        for g in gmap:
            if g in d:
                ans.append(1)
            else:
                ans.append(0)
        return ans 
        
    def fit(self, enc=LabelEncoder()):
        self.__df['kind'] = enc.fit_transform(self.__df['kind'])
        self.__df['rating'] = enc.fit_transform(self.__df['rating'])
        gmap = self.__df['genres'].fillna('genres_unknow').str.split(',').explode().unique()
        self.__df['genres'] = self.__df['genres'].str.split(',')
        self.__df['genres'] = self.__df['genres'].fillna('genres_unknown')
        arr = []
        for i in self.__df.index:
            arr.append(self.oh(gmap, self.__df['genres'][i]))
        self.__df = pd.concat([self.__df, pd.DataFrame(arr, columns = gmap)], axis=1)
        feat = np.append(gmap, ['kind', 'rating'])
        smd = self.__df[feat]
        self.__sim_matrix = cosine_similarity(smd, smd)
        
    def predict(self, title):
            indices = pd.Series(dict(zip(tuple(self.__df['russian']), self.__df.index)))
            titles = self.__df[['name', 'russian', 'wr', 'kind']]
            idx = indices[title]
            sim_scores = list(enumerate(self.__sim_matrix[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:31]
            title_indices = [i[0] for i in sim_scores]
            ans = titles.iloc[title_indices].sort_values(by='wr', ascending=False)
            ans = ans['russian']
            return ans

if __name__ == '__main__':
    rec = I2I_Recs()
    rec.fit()
    with open('similitary.pkl', 'wb') as f:
       pickle.dump(rec, f)
    
    
