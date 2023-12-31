import argparse
import pickle
from pathlib import Path

import polars as pl
import pandas as pd
import numpy as np

from my_model import MyALSModel
from my_encoder import MyEncoder

def fit(config) -> None:
    print("Train events:")
    train_events = pd.read_csv(config.data_dir / "interactions.csv",names=['user_id', 'user_name', 'rating', 'datetime', 'item_id', 'item_name', 'item_russian'])
    print(train_events)

    print("Items:")
    items = pd.read_csv(config.data_dir / "items.csv", names=['id', 'name', 'russian', 'kind', 'item_episodes', 'item_aired', 'item_score'])
    print(items)
    print('Users:')
    users = pd.read_csv(config.data_dir / "users.csv", names=['user_id', 'sex', 'age'])
    print(users)

    encoder = MyEncoder(train_events, users, items)
    train_events, users, items, mapper = encoder.transform()

    train_events = pl.from_pandas(train_events)
    users = pl.from_pandas(users)
    items = pl.from_pandas(items)

    my_model = MyALSModel(n_factors=128, iterations=10, top_k=20, mapper=mapper)
    my_model.fit(train_events, users, items)

    config.model_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving trained model to {config.model_dir / 'als.pickle'}")
    with open(config.model_dir / "als.pickle", "bw") as f:
        pickle.dump(my_model, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_dir", type=Path, required=True, help="Path to directory with input data")
    parser.add_argument("-m", "--model_dir", type=Path, required=True, help="Path to model directory with the data need to be passed between fit and predict")
    parser.add_argument("-o", "--output_dir", type=Path, required=True, help="Path to output files with predictions")
    fit(parser.parse_args())


if __name__ == "__main__":
    main()
