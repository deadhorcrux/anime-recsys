

import pandas as pd
import numpy as np
import typing

class MyEncoder:
    def __init__(self, events: pd.DataFrame, users: pd.DataFrame, items: pd.DataFrame) -> None:
        self._events = events
        self._users = users
        self._items = items

    def transform(self):
        self._items['kind'] = self._items['kind'].fillna('kind_unknown')

        self._users['age'] = pd.qcut(self._users['age'], 4, labels=['6_24', '24_26', '26_29', '29_35']).astype('category')
        self._users['age'] = self._users['age'].cat.add_categories('age_unknown')
        self._users['age'] = self._users['age'].fillna('age_unknown')
        self._users['sex'] = np.array(self._users['sex'].astype(str))
        self._users['sex'] = self._users['sex'].fillna('sex_unknown')

        self._events['weight'] = np.ones(self._events.shape[0])
        self._events = self._events[['weight', 'datetime', 'user_id', 'item_id', 'rating']]

        item_titles = pd.Series(self._items['russian'].values, index=self._items['id']).to_dict()

        return self._events, self._users, self._items[['id', 'kind', 'item_episodes', 'item_score']], item_titles