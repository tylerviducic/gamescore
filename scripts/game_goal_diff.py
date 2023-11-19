import pandas as pd
import numpy as np
import glob

df = pd.read_csv(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/whole_season/all_player_games.csv')

df['game_goal_diff'] = np.where(
    'home_or_away' == 'HOME', df['home_score'] - df['away_score'], df['away_score'] - df['home_score'])

df.to_csv(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/whole_season/all_player_games.csv')
