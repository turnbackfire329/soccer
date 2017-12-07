""" Helper methods """

import datetime


SORT_OPTIONS = {
    "POINTS": "points",
    "GOALS": "goals",
    "GOALS_AGAINST": "goalsAgainst",
    "DIFFERENCE": "goalDifference"
}

LEAGUE_CODES: ['BL1', 'BL2', 'BL3', 'PL', 'EL1', 'ELC', 'PD', 'SD', 'SA', 'SB', 'FL1', 'FL2']

def get_season_from_date(date):
    if date.month < 8:
        return date.year - 1
    else:
        return date.year


def get_current_season():
    return get_season_from_date(datetime.date.today())

def get_current_decade():
    current_season = get_season_from_date(datetime.date.today())
    current_decade = int(str(current_season)[:-1] + "0")
    return current_decade

def get_empty_team_standings():
    return {
        "goals": 0,
        "goalsAgainst": 0,
        "points": 0,
        "playedGames": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goalsDifference": 0,
        "home": {
            "goals": 0,
            "goalsAgainst": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        },
        "away": {
            "goals": 0,
            "goalsAgainst": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        }
    }

def get_season_range(startDate, endDate):
    return list(range(get_season_from_date(startDate), get_season_from_date(endDate) + 1))