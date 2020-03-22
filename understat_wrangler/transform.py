import json
import pandas as pd

def parse_json(json_data):
    """ Takes in raw JSON data, and returns Python list/dictionary """
    data = json_data.replace('\'', '\"')
    parsed_data = json.loads(data)
    return parsed_data


def convert_json_to_dataframe(json_data):
    """
    Converts raw JSON data into Pandas DataFrame.
    """
    dataframe = pd.read_json(json_data)
    return dataframe


def get_team_name_from_dict(data):
    """
    Definition:
        Gets name of team from JSON dictionary, wherein the key is 'title'.
        i.e; Parses the JSON; searches for key='title', and returns name of team.
    Parameters:
        - Takes in JSON string as input.
    Returns:
        Name of team (str)
    """
    data = str(data).replace('\'', '\"')
    data = json.loads(data)
    team_name = data['title']
    return team_name


def get_home_away_info(data, flag):
    """
    Definition:
        Gets home/away info from JSON dictionary, wherein the keys are 'h' and 'a'
    Parameters:
        flag options are: ['H', 'A'] to get the HomeInfo and AwayInfo respectively.
    """
    flag = flag.strip().upper()
    data = str(data).replace('\'', '\"')
    data = json.loads(data)
    home = data['h']
    away = data['a']
    if flag == 'H':
        return home
    elif flag == 'A':
        return away
    return None


def get_forecast_info(data, flag):
    """
    Definition:
        Gets forecast info from JSON dictionary, wherein the keys are 'w', 'l' and 'd'
    Parameters:
        flag options are: ['H', 'A', 'D'] to get the forcasted HomeWinPercent, AwayWinPercent
        and DrawPercent respectively.
    Returns:
        Number (float) rounded off to 2 points, indicating either HomeWinPercent/AwayWinPercent/DrawPercent
    """
    flag = flag.strip().upper()
    data = str(data).replace('\'', '\"')
    data = json.loads(data)
    home_win_percent = round(float(data['w']) * 100, 2)
    away_win_percent = round(float(data['l']) * 100, 2)
    draw_percent = round(float(data['d']) * 100, 2)
    if flag == 'H':
        return home_win_percent
    elif flag == 'A':
        return away_win_percent
    elif flag == 'D':
        return draw_percent
    return None


def wrangle_list_to_dataframe(list_data):
    """
    Definition:
        Takes in list of dictionaries, and converts it to Pandas DataFrame.
        Sorts date/datetime column in ascending order.
    """
    dataframe = pd.DataFrame(data=list_data)
    columns = dataframe.columns.tolist()
    if 'date' in columns:
        dataframe = dataframe.sort_values(by='date', ascending=True).reset_index(drop=True)
    elif 'datetime' in columns:
        dataframe = dataframe.sort_values(by='datetime', ascending=True).reset_index(drop=True)
    return dataframe


def wrangle_upcoming_fixtures(dataframe):
    """
    Definition:
        Wrangle/pre-process upcoming fixtures data.
        Sorts datetime column in ascending order.
    """
    dataframe_new = pd.DataFrame()
    dataframe_new['datetime'] = dataframe['datetime']
    dataframe_new['HomeTeam'] = dataframe['h'].apply(get_team_name_from_dict)
    dataframe_new['AwayTeam'] = dataframe['a'].apply(get_team_name_from_dict)
    dataframe_new = dataframe_new.sort_values(by='datetime', ascending=True).reset_index(drop=True)
    return dataframe_new


def wrangle_results(dataframe):
    """
    Definition:
        Wrangle/pre-process results data.
        Sorts datetime column in ascending order.
    """
    dataframe_new = pd.DataFrame()
    dataframe_new['datetime'] = dataframe['datetime']
    dataframe_new['HomeTeam'] = dataframe['h'].apply(get_team_name_from_dict)
    dataframe_new['AwayTeam'] = dataframe['a'].apply(get_team_name_from_dict)
    dataframe_new['HomeGoals'] = dataframe['goals'].apply(get_home_away_info, args=['H'])
    dataframe_new['AwayGoals'] = dataframe['goals'].apply(get_home_away_info, args=['A'])
    dataframe_new['Home_xG'] = dataframe['xG'].apply(get_home_away_info, args=['H'])
    dataframe_new['Away_xG'] = dataframe['xG'].apply(get_home_away_info, args=['A'])
    dataframe_new['ForecastedHomeWinPercent'] = dataframe['forecast'].apply(get_forecast_info, args=['H'])
    dataframe_new['ForecastedAwayWinPercent'] = dataframe['forecast'].apply(get_forecast_info, args=['A'])
    dataframe_new['ForecastedDrawPercent'] = dataframe['forecast'].apply(get_forecast_info, args=['D'])
    dataframe_new = dataframe_new.sort_values(by='datetime', ascending=True).reset_index(drop=True)
    return dataframe_new


def wrangle_match_players(dict_data):
    """
    Definition:
        Wrangle/pre-process match player data i.e; players' data in particular match.
    """
    dataframe = pd.DataFrame()
    flag_home_away = ['h', 'a']
    for flag_h_a in flag_home_away:
        for h_a in list(dict_data[flag_h_a].keys()):
            dataframe_temp = pd.DataFrame(data=dict_data[flag_h_a][h_a], index=[0])
            dataframe = pd.concat(objs=[dataframe, dataframe_temp], ignore_index=True, sort=False)
    return dataframe


def wrangle_match_shots(dict_data):
    """
    Definition:
        Wrangle/pre-process match shots data i.e; players' shots-data in particular match.
    """
    dataframe = pd.DataFrame()
    flag_home_away = ['h', 'a']
    for h_a in flag_home_away:
        dataframe_temp = pd.DataFrame(data=dict_data[h_a])
        dataframe = pd.concat(objs=[dataframe, dataframe_temp], ignore_index=True, sort=False)
    dataframe = dataframe.sort_values(by='minute', ascending=True).reset_index(drop=True)
    return dataframe


def get_max_min_avg_exploded(data, flag):
    """
    Definition:
        Helper function that gets data from JSON dictionary, wherein the keys are 'max', 'min' and 'avg'.
    Parameters:
        flag options are: ['maximum', 'minimum', 'average'] to get the maximum, minimum
        and average values respectively.
    """
    flag = flag.strip().lower()
    data = str(data).replace('\'', '\"')
    data = json.loads(data)
    maximum = float(data['max'])
    minimum = float(data['min'])
    average = float(data['avg'])
    if flag == 'maximum':
        return maximum
    elif flag == 'minimum':
        return minimum
    elif flag == 'average':
        return average
    return None


def wrangle_max_min_avg(dataframe):
    """
    Definition:
        Takes in Pandas DataFrame, explodes the columns which contain dictionaries
        as values, and returns cleaned ['maximum', 'minimum', 'average'] data.
    """
    dataframe_new = pd.DataFrame()
    columns_to_explode = dataframe.columns.tolist()
    flags = ['maximum', 'minimum', 'average']
    if 'position' in columns_to_explode:
        columns_to_explode.remove('position')
    for column in columns_to_explode:
        for flag in flags:
            column_new = column + '_' + flag
            dataframe_new[column_new] = dataframe[column].apply(get_max_min_avg_exploded, args=[flag])
    dataframe_new['position'] = dataframe['position']
    return dataframe_new


def get_shots_goals_xg(data_dict, flag):
    """
    Helper function to get 'shots', 'goals', 'xG' from dictionary
    """
    if flag == 'shots':
        return data_dict[flag]
    elif flag == 'goals':
        return data_dict[flag]
    elif flag == 'xG':
        return data_dict[flag]
    return None


def wrangle_against_data(dataframe):
    """
    Definition:
        Takes in Pandas DataFrame, and returns cleaned-up 'against' data - after converting
        from dictionary to DataFrame format for ['shots', 'goals', 'xG'] columns.
    """
    stats = ['shots', 'goals', 'xG']
    for stat in stats:
        stat_new = stat + '_against'
        dataframe[stat_new] = dataframe['against'].apply(get_shots_goals_xg, args=[stat])
    dataframe.drop(labels=['against'], axis=1, inplace=True)
    return dataframe


def wrangle_team_stats(dict_raw_team_stats, team_name, season):
    """
    Definition:
        Wrangles stats of results for a particular team, by ['team_name', 'season']
    Returns:
        Dictionary of stats; wherein keys are stats, and values are DataFrames of the same.
    """
    dictionary_stats = dict()
    stats = list(dict_raw_team_stats.keys())
    for stat in stats:
        data_by_stat = pd.DataFrame(data=dict_raw_team_stats[stat]).T\
                                                                   .reset_index()\
                                                                   .rename({'index': stat}, axis=1)
        data_by_stat = wrangle_against_data(dataframe=data_by_stat)
        data_by_stat['team_name'] = team_name
        data_by_stat['season'] = season
        dictionary_stats[stat] = data_by_stat
    return dictionary_stats



def wrangle_player_grouped_stats(dict_player_grouped_stats):
    """
    Definition:
        Takes in raw dictionary of player grouped stats.
    Returns:
        Cleaned dictionary; wherein keys are stats, and values are cleaned DataFrames of the same.
    """
    dictionary_player_grouped_stats = dict()
    df_by_season = pd.DataFrame(data=dict_player_grouped_stats['season'])
    df_by_season.sort_values(by='season', ascending=True, inplace=True)
    dictionary_player_grouped_stats['season'] = df_by_season
    
    substats_to_cleanup = ['position', 'situation', 'shotZones', 'shotTypes']
    for substat in substats_to_cleanup:
        data_dirty = pd.DataFrame(data=dict_player_grouped_stats[substat])
        rows, cols = data_dirty.shape
        
        df_by_substat_cleaned = pd.DataFrame()
        for row in range(rows):
            for col in range(cols):
                data_dict = data_dirty.iloc[row].iloc[col]
                if type(data_dict) == dict:
                    data_by_subdict = pd.DataFrame(data=data_dict, index=[0])
                    df_by_substat_cleaned = pd.concat(objs=[df_by_substat_cleaned, data_by_subdict],
                                                      ignore_index=True,
                                                      sort=False)
        if 'season' in df_by_substat_cleaned.columns.tolist():
            df_by_substat_cleaned.sort_values(by='season', ascending=True, inplace=True)
        dictionary_player_grouped_stats[substat] = df_by_substat_cleaned
    return dictionary_player_grouped_stats