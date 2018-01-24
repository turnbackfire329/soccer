# Sample Test passing with nose and pytest

import datetime
from .context import soccer

MONGO_SETTINGS = {
    "MONGODB_SERVER": "localhost",
    "MONGODB_PORT": 27017,
    "MONGODB_DB": "soccer-test",
    "MONGODB_AUTH_DB": "user-data",
    "MONGODB_USER": "soccer",
    "MONGODB_PASSWORD": "kickoffpassshootgoal"
}

soc = soccer.Soccer(mongo_settings=MONGO_SETTINGS)
writer = soccer.writers.BasicWriter()
dc = soccer.data_connectors.data_connector.DataConnector()
fdo = soccer.data_connectors.FDOConnector()
    
def test_search_team():
    teams = soc.search_team("borussia")
    print(teams)

def test_search_player():
    players = soc.search_player("Götze")
    print(players)

def test_season_date():
    assert soccer.util.get_season_from_date(datetime.date(2015,4,29)) == 2014

def test_table():
    standings = soc.get_league_table("BL1", season="2016", home=True, away=True)
    assert standings["standing"][2]["goals"] == 72

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