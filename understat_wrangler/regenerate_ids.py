import utils
import pipeline
import datetime
import numpy as np
import pandas as pd


def get_team_ids_dictionary():
    """
    Gets dictionary of Team-IDs wherein keys are IDs and values are Team-names.
    """
    df_team_id_data = pd.DataFrame()
    current_year = int(datetime.datetime.now().year)
    seasons = np.arange(start=2014, stop=current_year+1, step=1)
    league_names = ['Bundesliga', 'EPL', 'Serie A', 'La Liga', 'Ligue 1']
    for league_name in league_names:
        for season in seasons:
            df_teams_data_by_league = pipeline.get_teams_data(league_name=league_name,
                                                              season=season,
                                                              options=None)
            df_team_id_data = pd.concat(objs=[df_team_id_data, df_teams_data_by_league],
                                        ignore_index=True,
                                        sort=False)
    df_team_id_data = utils.convert_dtypes(dataframe=df_team_id_data,
                                           columns=['id'],
                                           dtypes=[str])
    df_team_id_data.drop_duplicates(subset=['id'], keep='first', inplace=True)
    dict_team_id_data = df_team_id_data.set_index('id').to_dict()['title']
    return dict_team_id_data


def get_player_ids_dictionary():
    """
    Gets dictionary of Player-IDs wherein keys are IDs and values are Player-names.
    """
    df_player_id_data = pd.DataFrame()
    current_year = int(datetime.datetime.now().year)
    seasons = np.arange(start=2014, stop=current_year+1, step=1)
    league_names = ['Bundesliga', 'EPL', 'Serie A', 'La Liga', 'Ligue 1']
    for league_name in league_names:
        for season in seasons:
            df_players_data_by_league = pipeline.get_league_players_data(league_name=league_name,
                                                                         season=season,
                                                                         options=None)
            df_players_data_by_league = df_players_data_by_league.loc[:, ['id', 'player_name']]
            df_player_id_data = pd.concat(objs=[df_player_id_data, df_players_data_by_league],
                                          ignore_index=True,
                                          sort=False)
    df_player_id_data = utils.convert_dtypes(dataframe=df_player_id_data,
                                             columns=['id'],
                                             dtypes=[str])
    df_player_id_data.drop_duplicates(subset=['id'], keep='first', inplace=True)
    dict_player_id_data = df_player_id_data.set_index('id').to_dict()['player_name']
    return dict_player_id_data


def generate_all_ids():
    """ Generate and store IDs of Teams and Players """
    # Teams
    dict_team_ids = get_team_ids_dictionary()
    utils.pickle_save(data_obj=dict_team_ids, filename='ids_of_teams.pkl')
    
    # Players
    dict_player_ids = get_player_ids_dictionary()
    utils.pickle_save(data_obj=dict_player_ids, filename='ids_of_players.pkl')
    return None


if __name__ == "__main__":
    try:
        time_taken = utils.run_and_timeit(func=generate_all_ids)
        print("IDs for teams and players have been re-generated and stored in Pickle files")
        print("Time taken: {} minutes".format(time_taken))
    except Exception as e:
        print("Failed! ErrorMsg: {}".format(e))