# Sample Test passing with nose and pytest

import datetime
from .context import soccer

dc = soccer.data_connectors.data_connector.DataConnector()
    
def test_compute_goal_table():
    fixtures = [
        {
            "_id": "1",
            "goals":[{
                'player_id':1,
                'player_name': "Player #1",
                'type': 'goal',
                'team_id': 1,
            },{
                'player_id':1,
                'player_name': "Player #1",
                'type': 'goal',
                'team_id': 1,
            },],
            "assists": [{
                'player_id':2,
                'player_name': "Player #2",
                'type': 'goal',
                'team_id': 1,
            },{
                'player_id':3,
                'player_name': "Player #3",
                'type': 'goal',
                'team_id': 1,
            },],
            "lineups": {
                "home": {},
                "away": {},
            },
            "homeTeam": {
                "team_id": 1,
                "name": "Team 1",
            },
            "awayTeam": {
                "team_id": 2,
                "name": "Team 2",
            }
        }
    ]

    scorer_table = dc.compute_scorer_table(fixtures, goals=True, assists=True)
    assert len(scorer_table) == 3

def test_get_seasons_from_timeframe():
    timeframe = {
        "type": "date",
        "date_from": datetime.datetime.strptime("2011-01-01", '%Y-%m-%d'),
        "date_to": datetime.datetime.strptime("2014-01-01", '%Y-%m-%d'),
    }
    assert range(2010,2013) == dc._get_seasons_from_timeframe(timeframe)

def test_season_date():
    assert soccer.util.get_season_from_date(datetime.date(2015,4,29)) == 2014

def test_deep_get():
    d = {
        "1": {
            2: {
                '3': 42,
            },
        },
    }
    assert dc._deep_get(d, ["1", 2, '3']) == 42

def test_get_sort_tuple():
    sortBy = (['points'], ['goalDifference'], ['goals'], ['away', 'goals'])
    ascending = ascending = (-1, -1, -1, -1)
    x = {
        'goals': 8,
        'goalsAgainst': 0,
        'points': 24,
        'negative_points': 0,
        'playedGames': 8,
        'wins': 8,
        'draws': 0,
        'losses': 0,
        'goalDifference': 8,
        'home': {'goals': 4, 'goalsAgainst': 0, 'goalDifference': 4, 'wins': 4, 'draws': 0, 'losses': 0},
        'away': {'goals': 4, 'goalsAgainst': 0, 'goalDifference': 4, 'wins': 4, 'draws': 0, 'losses': 0},
        'teamName': 'Team 1',
        'teamId': 1
    }
    sort_tuple = dc._get_sort_tuple(x, sortBy, ascending)
    assert sort_tuple == (-24, -8, -8, -4)

def test_tie_break_rules():
    fixtures = [
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 1,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id": 1,
            },
            "awayTeam": {
                "team_id": 2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 1,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id":1,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":1,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":1,
            },
            "awayTeam": {
                "team_id":5,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":5,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":3,
                "goalsAwayTeam":2,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":5,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":3,
                "goalsAwayTeam":2,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":5,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":5,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":5,
            },
            "awayTeam": {
                "team_id":2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":5,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":5,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
    ]

    standings = dc.compute_team_standings(fixtures)

    standings = dc.sort_league_table(standings, fixtures)

    teams = []
    for standing in standings:
        teams.append(standing['teamId'])

    assert teams == [1,4,2,3,5]

def test_tie_break_rules_h2h():
    fixtures = [
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 3,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id": 1,
            },
            "awayTeam": {
                "team_id": 2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 3,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id":1,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":2,
            },
        },
    ]

    standings = dc.compute_team_standings(fixtures)

    standings = dc.sort_league_table(standings, fixtures, tie_break_rules=[
        'POINTS',
        'GOAL_DIFFERENCE',
        'GOALS',
        'POINTS_H2H',
        'GOAL_DIFFERENCE_H2H',
        'AWAY_GOALS_H2H',
        'AWAY_GOALS',
    ])

    teams = []
    for standing in standings:
        teams.append(standing['teamId'])

    assert teams == [1,3,2]

def test_tie_break_rules_h2h_and_away():
    fixtures = [
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 3,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id": 1,
            },
            "awayTeam": {
                "team_id": 2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 3,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id":1,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam": 1,
                "goalsAwayTeam": 0,
            },
            "homeTeam": {
                "team_id":1,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":2,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":2,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":0,
            },
            "homeTeam": {
                "team_id":3,
            },
            "awayTeam": {
                "team_id":4,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":1,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":0,
                "goalsAwayTeam":1,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":2,
            },
        },
        {
            "dateObject": datetime.datetime.now(),
            "result": {
                "goalsHomeTeam":1,
                "goalsAwayTeam":2,
            },
            "homeTeam": {
                "team_id":4,
            },
            "awayTeam": {
                "team_id":3,
            },
        },
    ]

    standings = dc.compute_team_standings(fixtures)

    standings = dc.sort_league_table(standings, fixtures, tie_break_rules=[
        'POINTS',
        'GOAL_DIFFERENCE',
        'GOALS',
        'POINTS_H2H',
        'GOAL_DIFFERENCE_H2H',
        'AWAY_GOALS_H2H',
        'AWAY_GOALS',
    ])

    teams = []
    for standing in standings:
        teams.append(standing['teamId'])

    assert teams == [1,3,2,4]