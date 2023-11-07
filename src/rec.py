

from typing import List, Dict, Optional
import pandas as pd 
import numpy as np

sim_matrix = np.load('../data/sim_matrix.npy')
indices = pd.read_pickle('../data/indices.pickle')
indices_orig = pd.read_pickle('../data/indices_orig.pickle')
titles = pd.read_pickle('../data/titles.pickle')
recs = pd.read_pickle('../data/recs.pickle')

def get_user_rec(user_name: str) -> List:
    user_recs = recs[recs['user_name'] == user_name]['title'].values
    return user_recs

def get_similitary_rec(title: str) -> Dict:
    title = title.lower()
    if title in indices.index:
        idx = indices[title]
    elif title in indices_orig.index:
        idx = indices_orig[title]
    else:
        return 'Я не знаю такое аниме :('
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    title_indices = [i[0] for i in sim_scores]
    ans = titles.iloc[title_indices].sort_values(by='wr', ascending=False)
    ans = ans['russian']
    ans = ans.to_dict()
    message = str('\n')
    for idx, item in enumerate(ans.values()):
        if idx == 10:
            break
        message += f"• {item} \n"
    return message

if __name__ == '__main__':
    print(get_similitary_rec('nAruto'))
    print(get_user_rec('morr'))
