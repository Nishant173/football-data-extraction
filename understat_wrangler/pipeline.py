import get_user_input
import utils
import extract
import transform
import json
import pandas as pd


def get_league_fixtures_data(league_name, season, options=None):
    """
    Get Pandas DataFrame of upcoming league fixtures, by ['league_name', 'season']
    """
    json_data = extract.get_league_fixtures(league_name=league_name, season=season, options=options)
    data_league_fixtures = transform.convert_json_to_dataframe(json_data=json_data)
    if data_league_fixtures.empty:
        return pd.DataFrame()
    data_league_fixtures = transform.wrangle_upcoming_fixtures(dataframe=data_league_fixtures)
    return data_league_fixtures


def get_league_players_data(league_name, season, options=None):
    """
    Get Pandas DataFrame of stats of players in same league, by ['league_name', 'season']
    """
    json_data = extract.get_league_players(league_name=league_name, season=season, options=options)
    data_league_players = transform.convert_json_to_dataframe(json_data=json_data)
    data_league_players['goals'] = data_league_players['goals'].astype(int)
    data_league_players['assists'] = data_league_players['assists'].astype(int)
    data_league_players = data_league_players.sort_values(by=['goals', 'assists'], ascending=[False, False])\
                                             .reset_index(drop=True)
    return data_league_players


def get_league_results_data(league_name, season, options=None):
    """
    Get Pandas DataFrame of all results (so far) of games in same league, by ['league_name', 'season']
    """
    json_data = extract.get_league_results(league_name=league_name, season=season, options=options)
    data_league_results = transform.convert_json_to_dataframe(json_data=json_data)
    data_league_results = transform.wrangle_results(dataframe=data_league_results)
    return data_league_results


def get_match_players_data(match_id, options=None):
    """
    Get Pandas DataFrame of stats of all players in a particular match, by ['match_id']
    """
    json_data = extract.get_match_players(match_id=match_id, options=options)
    dict_data = transform.parse_json(json_data=json_data)
    data_match_players = transform.wrangle_match_players(dict_data=dict_data)
    data_match_players['match_id'] = match_id
    team_ids_all = utils.pickle_load(filename='ids_of_teams.pkl')
    team_ids = data_match_players['team_id'].astype(str).unique().tolist()
    data_match_players.loc[data_match_players['team_id'] == team_ids[0], 'team_name'] = team_ids_all[team_ids[0]]
    data_match_players.loc[data_match_players['team_id'] == team_ids[1], 'team_name'] = team_ids_all[team_ids[1]]
    return data_match_players


def get_match_shots_data(match_id, options=None):
    """
    Get Pandas DataFrame of shots-data of all players in a particular match, by ['match_id']
    """
    json_data = extract.get_match_shots(match_id=match_id, options=options)
    dict_data = transform.parse_json(json_data=json_data)
    data_match_shots = transform.wrangle_match_shots(dict_data=dict_data)
    return data_match_shots


def get_player_grouped_stats_data(player_id):
    """
    Get dictionary of various stats of particular player, by ['player_id'].
    Includes multiple substats such as ['season', 'position', 'situation', 'shotZones', 'shotTypes']
    """
    json_data = extract.get_player_grouped_stats(player_id=player_id)
    parsed_dict_data = transform.parse_json(json_data=json_data)
    dict_player_grouped_stats_clean = transform.wrangle_player_grouped_stats(dict_player_grouped_stats=parsed_dict_data)
    player_ids_all = utils.pickle_load(filename='ids_of_players.pkl')
    player_name = player_ids_all[str(player_id)]
    for _, df_by_substat in dict_player_grouped_stats_clean.items():
        df_by_substat['PlayerName'] = player_name
    return dict_player_grouped_stats_clean


def get_player_matches_data(player_id, options=None):
    """
    Get Pandas DataFrame of stats of particular player in all matches he's played, by ['player_id']
    """
    json_data = extract.get_player_matches(player_id=player_id, options=options)
    list_of_matches = transform.parse_json(json_data=json_data)
    data_player_matches = transform.wrangle_list_to_dataframe(list_data=list_of_matches)
    player_ids_all = utils.pickle_load(filename='ids_of_players.pkl')
    player_name = player_ids_all[str(player_id)]
    data_player_matches['PlayerName'] = player_name
    return data_player_matches


def get_player_shots_data(player_id, options=None):
    """
    Get Pandas DataFrame of shots-data of particular player in all matches he's played, by ['player_id']
    """
    json_data = extract.get_player_shots(player_id=player_id, options=options)
    list_of_matches = transform.parse_json(json_data=json_data)
    data_player_shots = transform.wrangle_list_to_dataframe(list_data=list_of_matches)
    return data_player_shots


def get_player_stats_data(player_id, positions=None):
    """
    Get Pandas DataFrame of max, min, avg stats of player over the seasons, by ['player_id']
    """
    json_data = extract.get_player_stats(player_id=player_id, positions=positions)
    list_of_matches = transform.parse_json(json_data=json_data)
    data_player_stats = transform.wrangle_list_to_dataframe(list_data=list_of_matches)
    data_player_stats = transform.wrangle_max_min_avg(dataframe=data_player_stats)
    player_ids_all = utils.pickle_load(filename='ids_of_players.pkl')
    player_name = player_ids_all[str(player_id)]
    data_player_stats['PlayerName'] = player_name
    return data_player_stats


def get_stats_data(sort_by_date=False, options=None):
    """
    Get Pandas DataFrame of all league stats in the top 5 leagues, over time.
    Parameters:
        - sort_by_date (bool): Sort data by league names if False. Sort data by dates if True. Default: False
        - options (dict): options to filter out data to extract
    NOTE: Can be used for time-series analysis.
    """
    json_data = extract.get_stats(options=options)
    list_of_stats = transform.parse_json(json_data=json_data)
    data_stats = transform.wrangle_list_to_dataframe(list_data=list_of_stats)

    data_stats['year'] = data_stats['year'].astype(int)
    data_stats['month'] = data_stats['month'].astype(int)
    data_stats = data_stats.sort_values(by=['league', 'year', 'month'], ascending=[True, True, True])\
                           .reset_index(drop=True)
    
    data_stats['datetime'] = data_stats['year'].astype(str) + '-' + data_stats['month'].astype(str) + '-' + '28'
    data_stats['datetime'] = pd.to_datetime(arg=data_stats['datetime'], format="%Y-%m-%d")
    if sort_by_date:
        data_stats = data_stats.sort_values(by='datetime', ascending=True).reset_index(drop=True)
    return data_stats


def get_team_fixtures_data(team_name, season):
    """
    Get Pandas DataFrame of upcoming league fixtures for a particular team, by ['team_name', 'season']
    """
    data_new = pd.DataFrame()
    json_upcoming_fixtures_home = extract.get_team_fixtures(team_name=team_name, season=season, side='h')
    json_upcoming_fixtures_away = extract.get_team_fixtures(team_name=team_name, season=season, side='a')
    list_of_matches_home = transform.parse_json(json_data=json_upcoming_fixtures_home)
    list_of_matches_away = transform.parse_json(json_data=json_upcoming_fixtures_away)
    list_of_matches = list_of_matches_home + list_of_matches_away
    data = transform.wrangle_list_to_dataframe(list_data=list_of_matches)
    if data.empty:
        return pd.DataFrame()
    data_new = transform.wrangle_upcoming_fixtures(dataframe=data)
    data_new['h_a'] = data['side']
    data_new['TeamOfInterest'] = team_name
    return data_new


def get_team_players_data(team_name, season, options=None):
    """
    Get Pandas DataFrame of stats of players for a particular team, by ['team_name', 'season']
    """
    json_data = extract.get_team_players(team_name=team_name, season=season, options=options)
    list_of_players = transform.parse_json(json_data=json_data)
    data_team_players = transform.wrangle_list_to_dataframe(list_data=list_of_players)
    data_team_players['season'] = season
    return data_team_players


def get_team_results_data(team_name, season, options=None):
    """
    Get Pandas DataFrame of stats of results for a particular team, by ['team_name', 'season']
    """
    data_team_results = pd.DataFrame()
    json_data = extract.get_team_results(team_name=team_name, season=season, options=options)
    list_of_matches = transform.parse_json(json_data=json_data)
    data = transform.wrangle_list_to_dataframe(list_data=list_of_matches)
    data_team_results = transform.wrangle_results(dataframe=data)    
    data_team_results['h_a'] = data['side']
    data_team_results['result'] = data['result'].map({
        'w': 'Win',
        'l': 'Loss',
        'd': 'Draw'
    })
    data_team_results['TeamOfInterest'] = team_name
    data_team_results['season'] = season
    data_team_results.sort_values(by='datetime', ascending=True, inplace=True)
    return data_team_results


def get_team_stats_data(team_name, season):
    """
    Get dictionary of stats of results for a particular team, by ['team_name', 'season']
    """
    json_data = extract.get_team_stats(team_name=team_name, season=season)
    dict_data = transform.parse_json(json_data=json_data)
    dict_team_stats = transform.wrangle_team_stats(dict_raw_team_stats=dict_data,
                                                   team_name=team_name,
                                                   season=season)    
    return dict_team_stats


def get_teams_data(league_name, season, options=None):
    """
    Get Pandas DataFrame of just 'id', 'title' columns - Indicating the TeamIDs
    """
    json_data = extract.get_teams(league_name=league_name, season=season, options=options)
    list_data = transform.parse_json(json_data=json_data)
    data_teams = pd.DataFrame(data=list_data)
    data_teams = data_teams.loc[:, ['id', 'title']]
    return data_teams



def execute_pipeline():
    """
    Function that executes the entire pipeline of the following:
        - Extraction of raw JSON data
        - Transformation of raw JSON data into human readable/understandable Excel/CSV files
        - Storage of these Excel/CSV files into a results folder
    """
    print("Processing...")
    dict_user_input = get_user_input.read_user_input()

    season = int(dict_user_input['season'])
    season_to_store = f"{str(season)}-{str(season + 1)[2:]}"
    league_name = dict_user_input['league_name']
    team_name = dict_user_input['team_name']
    match_id = str(dict_user_input['match_id'])
    player_id = str(dict_user_input['player_id'])
    
    player_ids_all = utils.pickle_load(filename='ids_of_players.pkl')
    player_name = player_ids_all[player_id].replace(' ', '')
    options = None
    positions = None

    dict_function_calls = {
        'upcoming_league_fixtures': get_league_fixtures_data(league_name=league_name,
                                                             season=season,
                                                             options=options),
        'league_players': get_league_players_data(league_name=league_name,
                                                  season=season,
                                                  options=options),
        'league_results': get_league_results_data(league_name=league_name,
                                                  season=season,
                                                  options=options),
        'match_players': get_match_players_data(match_id=match_id, options=options),
        'match_shots': get_match_shots_data(match_id=match_id, options=options),
        'player_grouped_stats': get_player_grouped_stats_data(player_id=player_id),
        'player_matches': get_player_matches_data(player_id=player_id, options=options),
        'player_shots': get_player_shots_data(player_id=player_id, options=options),
        'player_stats': get_player_stats_data(player_id=player_id, positions=positions),
        'stats': get_stats_data(sort_by_date=False, options=options),
        'upcoming_team_fixtures': get_team_fixtures_data(team_name=team_name, season=season),
        'team_players': get_team_players_data(team_name=team_name, season=season, options=options),
        'team_results': get_team_results_data(team_name=team_name, season=season, options=options),
        'team_stats': get_team_stats_data(team_name=team_name, season=season)
    }

    dict_filenames_to_store = {
        'upcoming_league_fixtures': f'Upcoming league fixtures - {season_to_store} - {league_name}',
        'league_players': f'League players - {season_to_store} - {league_name}',
        'league_results': f'League results - {season_to_store} - {league_name}',
        'match_players': f'Match players - MatchID{match_id}',
        'match_shots': f'Match shots - MatchID{match_id}',
        'player_grouped_stats': f'Player grouped stats - {player_id}{player_name}',
        'player_matches': f'Player matches - {player_id}{player_name}',
        'player_shots': f'Player shots - {player_id}{player_name}',
        'player_stats': f'Player stats - {player_id}{player_name}',
        'stats': f'All league stats - TimeSeries',
        'upcoming_team_fixtures': f'Upcoming team fixtures - {season_to_store} - {team_name}',
        'team_players': f'Team players - {season_to_store} - {team_name}',
        'team_results': f'Team results - {season_to_store} - {team_name}',
        'team_stats': f'Team stats - {season_to_store} - {team_name}'
    }

    utils.create_global_results_folder()
    
    for stat, func_call in dict_function_calls.items():
        try:
            if stat in ['team_stats', 'player_grouped_stats']:
                data_dict = func_call
                for sub_stat, sub_df in data_dict.items():
                    if not sub_df.empty:
                        name = dict_filenames_to_store[stat] + f" - {sub_stat}"
                        utils.save_data_to_csv(dataframe=sub_df, name=name)
            else:
                df = func_call
                if not df.empty:
                    name = dict_filenames_to_store[stat]
                    utils.save_data_to_csv(dataframe=df, name=name)
        except Exception as e:
            print("Problem with stat: {} --> ErrorMsg: {}".format(stat, e))
    return None