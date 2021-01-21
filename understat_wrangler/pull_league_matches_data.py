from pipeline import get_league_results_data


if __name__ == "__main__":
    leagues = ['Bundesliga', 'EPL', 'La Liga', 'Ligue 1', 'Serie A']
    countries = ['Germany', 'England', 'Spain', 'France', 'Italy']
    seasons = [2020] * len(leagues) # Enter 2014 for 2014-15 season
    for league_name, season, country in zip(leagues, seasons, countries):
        season_string = f"{season}-{str(season + 1)[2:]}"
        df_league_results = get_league_results_data(league_name=league_name, season=season)
        df_league_results['Country'] = country
        df_league_results['League'] = league_name
        df_league_results['Season'] = season_string
        df_league_results.rename({'datetime': 'Date'}, axis=1, inplace=True)
        df_league_results['Date'] = df_league_results['Date'].dt.strftime(date_format="%m/%d/%Y")
        columns = ['HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals', 'Country', 'League', 'Season', 'Date']
        df_league_results = df_league_results.loc[:, columns]
        df_league_results.to_csv(f"{league_name} - {season_string}.csv", index=False)