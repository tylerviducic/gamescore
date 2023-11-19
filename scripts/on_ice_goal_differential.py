import pandas as pd
import numpy as np
import glob


files = glob.glob(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/whole_season/*.csv')

df = pd.concat([pd.read_csv(f) for f in files])

df['on_ice_goal_diff'] = np.where(
    True, df['OnIce_F_goals'] - df['OnIce_A_goals'], 0)
df['on_ice_xgoal_diff'] = np.where(
    True, df['OnIce_F_xGoals'] - df['OnIce_A_xGoals'], 0)

df.to_csv(
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/cleaned_data/whole_season/all_player_games.csv')
