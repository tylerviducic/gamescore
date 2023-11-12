import os
import sys
sys.path.append(os.path.abspath(os.path.join(  # noqa
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model')))  # noqa
import utils.helper_funcs as helper
import pandas as pd
import numpy as np


df = pd.read_csv(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv')

df['season'] = np.where(
    True, df['game_id']/100000, 0).astype(int)

df.to_csv('/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv', index=False)
