import os
import sys
sys.path.append(os.path.abspath(os.path.join(  # noqa
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model')))  # noqa
import utils.helper_funcs as helper
import pandas as pd
import numpy as np
import glob

files = glob.glob(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/odd_games/*.csv')

last = helper.status_bar(0, len(files), 0)
avg_dif_dict = {}

for file in files:
    df = pd.read_csv(file)
    df['goal_diff'] = np.where(df['home_or_away'] == 'HOME', df['home_score'] -
                               df['away_score'], df['away_score'] - df['home_score'])
    grouped = df.groupby('season')
    for name, group in grouped:
        avg_dif_dict[name] = group['goal_diff'].mean()

    df['season_avg_goal_diff'] = df['season'].map(avg_dif_dict)
    df.to_csv(file, index=False)
    last = helper.status_bar(files.index(file) + 1, len(files), last)
