

import sys 
import csv
from csv import writer
import pandas as pd
import time 
import json
from shikimori_api import Shikimori

if __name__ == '__main__':
    session = Shikimori()
    api = session.get_api()
    got, lost = 0, 0
    for i in range(1, 100000):
        users = []
        user_id = []
        item_id = []
        item_name = []
        item_russian = []
        nick = []
        rating = []
        timestamp = []
        info_id = []
        info_sex = []
        info_age = []
        info_online = [] 
        item_kind = []
        item_episodes = []
        item_aired = [] 
        item_score = []
        try:
            got+=1
            print('users got {}'.format(got))
            users.append(api.users(i).anime_rates.GET(limit=500))
            user = api.users(i).GET()
            info_id.append(user['id'])
            info_sex.append(user['sex'])
            info_age.append(user['full_years'])
            info_online.append(user['last_online'])
        except:
            lost+=1
            print('users lost {}'.format(lost))
        for i in users:
            for j in i:
                user_id.append(j['user']['id'])
                nick.append(j['user']['nickname'])
                rating.append(j['score'])
                timestamp.append(j['created_at'][:10])
                item_id.append(j['anime']['id'])
                item_name.append(j['anime']['name'])
                item_russian.append(j['anime']['russian'])
                item_kind.append(j['anime']['kind'])
                item_episodes.append(j['anime']['episodes'])
                item_aired.append(j['anime']['aired_on'])
                item_score.append(j['anime']['score'])
        df_users = pd.DataFrame(zip(info_id, info_sex, info_age), columns=['user_id', 'sex', 'age']) 
        df = pd.DataFrame(zip(user_id,  nick, rating, timestamp, item_id, item_name, item_russian), columns = ['user_id', 'user_name', 'rating', 'timestamp', 'item_id', 'item_name', 'item_russian'])
        df_items = pd.DataFrame(zip(item_id, item_name, item_russian, item_kind, item_episodes, item_aired, item_score), columns = ['item_id', 'item_name', 'item_russian', 'item_kind', 'item_episodes', 'item_aired', 'item_score'])
        df.to_csv('interactions.csv', mode='a', index=False, header=False)
        df_users.to_csv('users.csv', mode='a', index=False, header=False)
        df_items.to_csv('items.csv', mode='a', index=False, header=False)
    sys.exit(0)
