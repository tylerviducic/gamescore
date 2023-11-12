import os
import sys
sys.path.append(os.path.abspath(os.path.join(  # noqa
    '/Users/tylerviducic/dev/hockey_analytics/gamescore_model')))  # noqa
import utils.helper_funcs as helper
import pandas as pd
import numpy as np


def calculate_average_goal_diff(team_id):
    seasons = []
    avg_goal_diffs = []
    teams = []
    team_names = []
    df = pd.read_csv(
        '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv')
    team_df = df.loc[(df['home_team_id'] == team_id) |
                     (df['away_team_id'] == team_id)]
    grouped_df = team_df.groupby('season')
    team_name = helper.team_name_dict[team_id]
    for name, group in grouped_df:
        avg_goal_diff = np.where(group['home_team_id'] == team_id,
                                 group['home_goal_dif'], -1 * group['home_goal_dif']).mean()
        seasons.append(name)
        avg_goal_diffs.append(avg_goal_diff)
        teams.append(team_id)
        team_names.append(team_name)

    return pd.DataFrame({
        'season': seasons,
        'avg_goal_diff': avg_goal_diffs,
        'team_id': teams,
        'team_name': team_names
    })


if __name__ == '__main__':
    all_team_df = pd.concat(calculate_average_goal_diff(team_id)
                            for team_id in helper.team_name_dict)

    all_team_df.to_csv(
        '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/team_season_avg_goal_diff.csv')
