# Sample Test passing with nose and pytest

import datetime
from .context import soccer

soc = soccer.Soccer()
writer = soccer.writers.BasicWriter()
fdo = soccer.data_connectors.FDOConnector()

def test_season():
    assert soc._get_current_season() == 2017
    
def test_season_date():
    assert soc._get_season_from_date(datetime.date(2015,4,29)) == 2014

def test_table():
    standings = soc.get_league_table("BL1", season="2016", home=True, away=True)
    writer.league_table(standings)
    assert standings["standing"][2]["goals"] == 72

def test_sort_descending():
    standings = [
        {"points": 5, "goalDifference": 4, "goals": 7},
        {"points": 8, "goalDifference": 4, "goals": 7},
        {"points": 11, "goalDifference": 4, "goals": 7},
        {"points": 5, "goalDifference": 4, "goals": 8},
        {"points": 5, "goalDifference": 5, "goals": 7}
    ]
    assert fdo.sort_league_table(standings, (soccer.Soccer.SORT_OPTIONS["POINTS"], soccer.Soccer.SORT_OPTIONS["DIFFERENCE"], soccer.Soccer.SORT_OPTIONS["GOALS"])) == [
        {'goalDifference': 4, 'goals': 7, 'points': 11, 'position': 1},
        {'goalDifference': 4, 'goals': 7, 'points': 8, 'position': 2},
        {'goalDifference': 5, 'goals': 7, 'points': 5, 'position': 3},
        {'goalDifference': 4, 'goals': 8, 'points': 5, 'position': 4},
        {'goalDifference': 4, 'goals': 7, 'points': 5, 'position': 5}
    ]

def test_table_restricted_teams():
    standings = soc.get_league_table("BL1", season="2016", home=True, away=True, teams=[4,5,6], head2headOnly=True)
    writer.league_table(standings)
    assert True
