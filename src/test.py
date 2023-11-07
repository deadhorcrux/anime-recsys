

from typing import List, Dict, Optional
import pandas as pd 
import numpy as np

sim_matrix = np.load('../data/sim_matrix.npy')
indices = pd.read_pickle('../data/indices.pickle')
titles = pd.read_pickle('../data/titles.pickle')

def get_similitary_rec(item_name: str) -> Dict:
    idx = indices[title]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    title_indices = [i[0] for i in sim_scores]
    ans = titles.iloc[title_indices].sort_values(by='wr', ascending=False)
    ans = ans['russian']
    return ans.to_dict()

if __name__ == '__main__':
    title = 'Наруто'
    print(get_similitary_rec(title))
