import os
import sys
sys.path.append(os.path.abspath(os.path.join(  # noqa
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model')))  # noqa
import utils.helper_funcs as helper
import pandas as pd
import numpy as np


def get_home_goal_dif():
    df = pd.read_csv(
        '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv')
    df['home_goal_dif'] = np.where(
        True, df['home_goals'] - df['away_goals'], 0)
    return df


if __name__ == "__main__":
    df = get_home_goal_dif()
    df.to_csv(
        '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv', index=False)
