"""
functions used for building the model
"""

import pickle
from typing import final
import pandas as pd
import numpy as np
import cloudscraper
import io

from requests import get

team_id_dict = {
    'NJD': 1,
    'PHI': 4,
    'LAK': 26,
    'TBL': 14,
    'BOS': 6,
    'NYR': 3,
    'PIT': 5,
    'DET': 17,
    'SJS': 28,
    'NSH': 18,
    'VAN': 23,
    'CHI': 16,
    'OTT': 9,
    'MTL': 8,
    'MIN': 30,
    'WSH': 15,
    'STL': 19,
    'ANA': 24,
    'PHX': 27,
    'NYI': 2,
    'TOR': 10,
    'FLA': 13,
    'BUF': 7,
    'CGY': 20,
    'COL': 21,
    'DAL': 25,
    'CBJ': 29,
    'WPG': 52,
    'EDM': 22,
    'VGK': 54,
    'CAR': 12,
    'ARI': 53,
    'ATL': 11,
    'SEA': 55
}


def calculate_goal_dif(home_or_away, home_score, away_score):
    if home_or_away == 'HOME':
        return home_score - away_score
    else:
        return away_score - home_score


def normalize_data(df):
    norm_df = df.copy()
    for col in norm_df.columns:
        if norm_df.dtypes[col] == 'object':
            continue
        col_min = norm_df[col].min()
        col_max = norm_df[col].max()
        norm_df[col] = (norm_df[col] - col_min) / (col_max - col_min)
    return norm_df


def get_season_from_game_id(game_id):
    return int(str(game_id)[:4])


def calculate_team_season_goal_diff(player_team, season_start):
    final_scores = pd.read_csv(
        '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv')
    player_team_id = team_id_dict[player_team]
    final_scores['season'] = final_scores['game_id'].apply(
        get_season_from_game_id)
    team_season_scores = final_scores.loc[(final_scores['season'] == season_start) & (
        (final_scores['home_team_id'] == player_team_id) | (final_scores['away_team_id'] == player_team_id))]
    team_season_scores['home_or_away'] = team_season_scores.apply(
        lambda row: 'HOME' if row['home_team_id'] == player_team_id else 'AWAY', axis=1)
    team_season_scores['goal_dif'] = team_season_scores.apply(lambda row: calculate_goal_dif(
        row['home_or_away'], row['home_goals'], row['away_goals']), axis=1)
    return team_season_scores['goal_dif'].mean()


bio_labels = ['playerId', 'season', 'name', 'gameId', 'playerTeam',
              'opposingTeam', 'home_or_away', 'gameDate', 'position']
individual_skater_labels = ['icetime', 'shifts', 'gameScore', 'iceTimeRank', 'I_F_xOnGoal', 'I_F_xGoals', 'I_F_xRebounds', 'I_F_xFreeze', 'I_F_xPlayStopped', 'I_F_xPlayContinuedInZone', 'I_F_xPlayContinuedOutsideZone', 'I_F_flurryAdjustedxGoals', 'I_F_scoreVenueAdjustedxGoals', 'I_F_flurryScoreVenueAdjustedxGoals', 'I_F_primaryAssists', 'I_F_secondaryAssists', 'I_F_shotsOnGoal', 'I_F_missedShots', 'I_F_blockedShotAttempts', 'I_F_shotAttempts', 'I_F_points', 'I_F_goals', 'I_F_rebounds', 'I_F_reboundGoals', 'I_F_freeze', 'I_F_playStopped', 'I_F_playContinuedInZone', 'I_F_playContinuedOutsideZone', 'I_F_savedShotsOnGoal', 'I_F_savedUnblockedShotAttempts', 'penalties', 'I_F_penalityMinutes', 'I_F_faceOffsWon', 'I_F_hits', 'I_F_takeaways', 'I_F_giveaways', 'I_F_lowDangerShots', 'I_F_mediumDangerShots', 'I_F_highDangerShots',
                            'I_F_lowDangerxGoals', 'I_F_mediumDangerxGoals', 'I_F_highDangerxGoals', 'I_F_lowDangerGoals', 'I_F_mediumDangerGoals', 'I_F_highDangerGoals', 'I_F_scoreAdjustedShotsAttempts', 'I_F_unblockedShotAttempts', 'I_F_scoreAdjustedUnblockedShotAttempts', 'I_F_dZoneGiveaways', 'I_F_xGoalsFromxReboundsOfShots', 'I_F_xGoalsFromActualReboundsOfShots', 'I_F_reboundxGoals', 'I_F_xGoals_with_earned_rebounds', 'I_F_xGoals_with_earned_rebounds_scoreAdjusted', 'I_F_xGoals_with_earned_rebounds_scoreFlurryAdjusted', 'I_F_shifts', 'I_F_oZoneShiftStarts', 'I_F_dZoneShiftStarts', 'I_F_neutralZoneShiftStarts', 'I_F_flyShiftStarts', 'I_F_oZoneShiftEnds', 'I_F_dZoneShiftEnds', 'I_F_neutralZoneShiftEnds', 'I_F_flyShiftEnds', 'faceoffsWon', 'faceoffsLost', 'timeOnBench', 'penalityMinutes', 'penalityMinutesDrawn', 'penaltiesDrawn', 'shotsBlockedByPlayer']
on_ice_skater_labels = ['OnIce_F_xOnGoal', 'OnIce_F_xGoals', 'OnIce_F_flurryAdjustedxGoals', 'OnIce_F_scoreVenueAdjustedxGoals', 'OnIce_F_flurryScoreVenueAdjustedxGoals', 'OnIce_F_shotsOnGoal', 'OnIce_F_missedShots', 'OnIce_F_blockedShotAttempts', 'OnIce_F_shotAttempts', 'OnIce_F_goals', 'OnIce_F_rebounds', 'OnIce_F_reboundGoals', 'OnIce_F_lowDangerShots', 'OnIce_F_mediumDangerShots', 'OnIce_F_highDangerShots', 'OnIce_F_lowDangerxGoals', 'OnIce_F_mediumDangerxGoals', 'OnIce_F_highDangerxGoals', 'OnIce_F_lowDangerGoals', 'OnIce_F_mediumDangerGoals', 'OnIce_F_highDangerGoals', 'OnIce_F_scoreAdjustedShotsAttempts', 'OnIce_F_unblockedShotAttempts', 'OnIce_F_scoreAdjustedUnblockedShotAttempts', 'OnIce_F_xGoalsFromxReboundsOfShots', 'OnIce_F_xGoalsFromActualReboundsOfShots', 'OnIce_F_reboundxGoals', 'OnIce_F_xGoals_with_earned_rebounds', 'OnIce_F_xGoals_with_earned_rebounds_scoreAdjusted', 'OnIce_F_xGoals_with_earned_rebounds_scoreFlurryAdjusted',
                        'OnIce_A_xOnGoal', 'OnIce_A_xGoals', 'OnIce_A_flurryAdjustedxGoals', 'OnIce_A_scoreVenueAdjustedxGoals', 'OnIce_A_flurryScoreVenueAdjustedxGoals', 'OnIce_A_shotsOnGoal', 'OnIce_A_missedShots', 'OnIce_A_blockedShotAttempts', 'OnIce_A_shotAttempts', 'OnIce_A_goals', 'OnIce_A_rebounds', 'OnIce_A_reboundGoals', 'OnIce_A_lowDangerShots', 'OnIce_A_mediumDangerShots', 'OnIce_A_highDangerShots', 'OnIce_A_lowDangerxGoals', 'OnIce_A_mediumDangerxGoals', 'OnIce_A_highDangerxGoals', 'OnIce_A_lowDangerGoals', 'OnIce_A_mediumDangerGoals', 'OnIce_A_highDangerGoals', 'OnIce_A_scoreAdjustedShotsAttempts', 'OnIce_A_unblockedShotAttempts', 'OnIce_A_scoreAdjustedUnblockedShotAttempts', 'OnIce_A_xGoalsFromxReboundsOfShots', 'OnIce_A_xGoalsFromActualReboundsOfShots', 'OnIce_A_reboundxGoals', 'OnIce_A_xGoals_with_earned_rebounds', 'OnIce_A_xGoals_with_earned_rebounds_scoreAdjusted', 'OnIce_A_xGoals_with_earned_rebounds_scoreFlurryAdjusted']
all_strength_labels = bio_labels + individual_skater_labels


def get_score_of_game(game_id):
    df = pd.read_csv(
        '/Users/tylerviducic/dev/hockey_analytics/gamescore_model/data/kaggle_data/final_scores.csv')
    game_df = df.loc[df['game_id'] == game_id]
    try:
        home_score = game_df['home_goals'].values[0]
        away_score = game_df['away_goals'].values[0]
        return home_score, away_score
    except IndexError:
        print(f'IndexError: game_id {game_id} not found in final_scores.csv')
        return None, None
    except ValueError:
        print('wtf is going on')


def reduce_df(grouped_df):
    all_strength_df = pd.concat([group.loc[group['situation'] == 'all', all_strength_labels].reset_index(
        drop=True) for game, group in grouped_df])
    oi_5v5_frames_df = pd.concat([group.loc[group['situation'] == '5on5', on_ice_skater_labels].reset_index(
        drop=True) for game, group in grouped_df])
    reduced_df = pd.concat(
        [all_strength_df, oi_5v5_frames_df], axis=1).reset_index(drop=True)
    reduced_df = reduced_df[reduced_df['gameId'] < 2023000000]
    reduced_df[['home_score', 'away_score']] = reduced_df.apply(
        lambda row: get_score_of_game(row['gameId']), axis=1, result_type='expand')
    return reduced_df


def read_player_ids_from_pickle(pickle_filepath):
    with open(pickle_filepath, 'rb') as f:
        player_ids = pickle.load(f)
    return player_ids


def write_player_ids_to_pickle(player_ids, pickle_filepath):
    with open(pickle_filepath, 'wb') as f:
        pickle.dump(player_ids, f)


def status_bar(current, total, last):
    progress = int(current / total * 100)
    if current == 0:
        print('PROGRESS: [', end='', flush=True)
    if progress > last:
        print('\u2588', end='', flush=True)
    if current == total:
        print(']')
    return progress


def get_csv(url):
    with cloudscraper.CloudScraper() as scraper:
        csv = scraper.get(url)
        return io.StringIO(csv.content.decode('utf-8'))


if __name__ == "__main__":
    print(calculate_team_season_goal_diff('NJD', 2010))
