from pipeline import get_league_results_data


if __name__ == "__main__":
    leagues = ['Bundesliga', 'EPL', 'La Liga', 'Ligue 1', 'Serie A']
    seasons = [2020] * len(leagues)
    for league_name, season in zip(leagues, seasons):
        df_league_results = get_league_results_data(league_name=league_name, season=season)
        df_league_results.to_csv(f"{league_name} - {season}-{season+1}.csv", index=False)