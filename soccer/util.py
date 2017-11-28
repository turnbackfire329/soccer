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
