from understat import Understat
import asyncio
import aiohttp
import json


async def get_league_fixtures_async(league_name, season, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_fixtures(league_name=league_name,
                                                   season=season,
                                                   options=options)
        json_data = json.dumps(data)
    return json_data


def get_league_fixtures(league_name, season, options=None):
    """
    Returns a JSON list containing information about all the upcoming fixtures of
    the given league in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_league_fixtures_async(league_name=league_name,
                                                                  season=season,
                                                                  options=options))
    return json_data


async def get_league_players_async(league_name, season, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_players(league_name=league_name,
                                                  season=season,
                                                  options=options)
        json_data = json.dumps(data)
    return json_data


def get_league_players(league_name, season, options=None):
    """
    Returns JSON of a list containing information about all the players in
    the given league in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_league_players_async(league_name=league_name,
                                                                 season=season,
                                                                 options=options))
    return json_data


async def get_league_results_async(league_name, season, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_results(league_name=league_name,
                                                  season=season,
                                                  options=options)
        json_data = json.dumps(data)
    return json_data


def get_league_results(league_name, season, options=None):
    """
    Returns JSON of a list containing information about all the results (matches) played
    by the teams in the given league in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_league_results_async(league_name=league_name,
                                                                 season=season,
                                                                 options=options))
    return json_data


async def get_match_players_async(match_id, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_match_players(match_id=match_id,
                                                 options=options)
        json_data = json.dumps(data)
    return json_data


def get_match_players(match_id, options=None):
    """
    Returns JSON of a dictionary containing information about the players who played in the given match.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_match_players_async(match_id=match_id,
                                                                options=options))
    return json_data


async def get_match_shots_async(match_id, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_match_shots(match_id=match_id,
                                               options=options)
        json_data = json.dumps(data)
    return json_data


def get_match_shots(match_id, options=None):
    """
    Returns JSON of a dictionary containing information about shots taken by the players in the given match.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_match_shots_async(match_id=match_id,
                                                              options=options))
    return json_data


async def get_player_grouped_stats_async(player_id):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_player_grouped_stats(player_id=player_id)
        json_data = json.dumps(data)
    return json_data


def get_player_grouped_stats(player_id):
    """
    Returns JSON of grouped stats of the player with the given ID (as seen at the top of a player's page).
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_player_grouped_stats_async(player_id=player_id))
    return json_data


async def get_player_matches_async(player_id, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_player_matches(player_id=player_id,
                                                  options=options)
        json_data = json.dumps(data)
    return json_data


def get_player_matches(player_id, options=None):
    """
    Returns JSON of the matches of the player with the given ID.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_player_matches_async(player_id=player_id,
                                                                 options=options))
    return json_data


async def get_player_shots_async(player_id, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_player_shots(player_id=player_id,
                                                options=options)
        json_data = json.dumps(data)
    return json_data


def get_player_shots(player_id, options=None):
    """
    Returns JSON of the shots of the player with the given ID.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_player_shots_async(player_id=player_id,
                                                               options=options))
    return json_data


async def get_player_stats_async(player_id, positions=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_player_stats(player_id=player_id,
                                                positions=positions)
        json_data = json.dumps(data)
    return json_data


def get_player_stats(player_id, positions=None):
    """
    Returns JSON of the shots of the player with the given ID.
    Choices for positions: ['FW']
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_player_stats_async(player_id=player_id,
                                                               positions=positions))
    return json_data


async def get_stats_async(options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_stats(options=options)
        json_data = json.dumps(data)
    return json_data


def get_stats(options=None):
    """
    Returns JSON of a list containing stats of every league, for every year, grouped by month.
    Can be filtered by 'league' (str) and/or 'month' (str).
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_stats_async(options=options))
    return json_data


async def get_team_fixtures_async(team_name, season, side, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_team_fixtures(team_name=team_name,
                                                 season=season,
                                                 side=side,
                                                 options=options)
        json_data = json.dumps(data)
    return json_data


def get_team_fixtures(team_name, season, side, options=None):
    """
    Returns JSON of a team's upcoming home/away fixtures in the given season.
    The 'side' parameter can be one of ['h', 'a'].
    If 'side'='a', it gives fixtures wherein 'team_name' is away.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_team_fixtures_async(team_name=team_name,
                                                                season=season,
                                                                side=side,
                                                                options=options))
    return json_data


async def get_team_players_async(team_name, season, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_team_players(team_name=team_name,
                                                season=season,
                                                options=options)
        json_data = json.dumps(data)
    return json_data


def get_team_players(team_name, season, options=None):
    """
    Returns JSON of a team's players' statistics in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_team_players_async(team_name=team_name,
                                                               season=season,
                                                               options=options))
    return json_data


async def get_team_results_async(team_name, season, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_team_results(team_name=team_name,
                                                season=season,
                                                options=options)
        json_data = json.dumps(data)
    return json_data


def get_team_results(team_name, season, options=None):
    """
    Returns JSON of a team's results in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_team_results_async(team_name=team_name,
                                                               season=season,
                                                               options=options))
    return json_data


async def get_team_stats_async(team_name, season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_team_stats(team_name=team_name,
                                              season=season)
        json_data = json.dumps(data)
    return json_data


def get_team_stats(team_name, season):
    """
    Returns JSON of a team's stats, as seen on their page on Understat, in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_team_stats_async(team_name=team_name,
                                                             season=season))
    return json_data


async def get_teams_async(league_name, season, options=None):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_teams(league_name=league_name,
                                         season=season,
                                         options=options)
        json_data = json.dumps(data)
    return json_data


def get_teams(league_name, season, options=None):
    """
    Returns JSON of a list containing information about all the teams in the given
    league in the given season.
    """
    loop = asyncio.get_event_loop()
    json_data = loop.run_until_complete(get_teams_async(league_name=league_name,
                                                        season=season,
                                                        options=options))
    return json_data