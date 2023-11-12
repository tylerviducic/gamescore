import os
import sys
sys.path.append(os.path.abspath(os.path.join(  # noqa
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model')))  # noqa
import utils.helper_funcs as helper
import pandas as pd
import numpy as np
import glob


files = glob.glob(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/whole_season/*.csv')

last = helper.status_bar(0, len(files), 0)

for file in files:
    player_id = file.split('/')[-1].split('.')[0]
    df = pd.read_csv(file)
    even_df = df.iloc[::2]
    odd_df = df.iloc[1::2]
    if len(even_df) > len(odd_df):
        even_df = even_df.iloc[:-1]
    elif len(even_df) < len(odd_df):
        odd_df = odd_df.iloc[:-1]

    even_df.to_csv(
        f'/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/even_games/{player_id}.csv', index=False)
    odd_df.to_csv(
        f'/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/odd_games/{player_id}.csv', index=False)

    last = helper.status_bar(files.index(file) + 1, len(files), last)
