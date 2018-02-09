""" Helper methods """

import datetime
import pymongo
import configparser
import logging

import os

SORT_OPTIONS = {
    "POINTS": "points",
    "GOALS": "goals",
    "GOALS_AGAINST": "goalsAgainst",
    "DIFFERENCE": "goalDifference"
}

def get_settings(path=None):
    settings = {
        'mongodb_server': 'localhost',
        'mongodb_port': '27017',
        'mongodb_db': 'soccer-test',
        'mongodb_auth_db': 'user-data',
        'mongodb_user': 'soccer',
        'mongodb_password': 'kickoffpassshootgoal',
    }
    
    if path is not None:
        config = configparser.ConfigParser()
        config.read(path)

        settings['mongodb_server'] = config['DEFAULT'].get('mongodb_server', 'localhost')
        settings['mongodb_port'] = config['DEFAULT'].get('mongodb_port', '27017')
        settings['mongodb_db'] = config['DEFAULT'].get('mongodb_db', 'soccer-test')
        settings['mongodb_auth_db'] = config['DEFAULT'].get('mongodb_auth_db', 'user-data')
        settings['mongodb_user'] = config['DEFAULT'].get('mongodb_user', 'soccer')
        settings['mongodb_password'] = config['DEFAULT'].get('mongodb_password', 'kickoffpassshootgoal')
    
    return settings

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

def get_season_range(startDate, endDate):
    return list(range(get_season_from_date(startDate), get_season_from_date(endDate) + 1))

def season_to_string(season):
    first_year = int(season)
    second_year = first_year + 1

    return str(first_year) + "/" + str(second_year)[2:]

def make_ngrams(word, prefix_only=False):
    """
        string  word: word to split into ngrams
    """    
    min_size = 4
    length = len(word)
    size_range = range(min_size, max(length, min_size) + 1)
    if prefix_only:
        return [
            word[0:size]
            for size in size_range
        ]
    return list(set(
        word[i:i + size]
        for size in size_range
        for i in range(0, max(0, length - size) + 1)
    )) 

EMPTY_TEAM_STANDINGS = {
    "goals": 0,
    "goalsAgainst": 0,
    "points": 0,
    "negative_points": 0,
    "playedGames": 0,
    "wins": 0,
    "draws": 0,
    "losses": 0,
    "goalDifference": 0,
    "home": {
        "goals": 0,
        "goalsAgainst": 0,
        "goalDifference": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0
    },
    "away": {
        "goals": 0,
        "goalsAgainst": 0,
        "goalDifference": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
    },
}

DEFAULT_POINT_RULE = '3p'
DEFAULT_POINT_RULE_WIN_POINTS = 3
DEFAULT_POINT_RULE_DRAW_POINTS = 1
DEFAULT_POINT_RULE_DISPLAY_NEGATIVE_POINTS = False

POINT_RULES = {
    '2p': {
        'WIN_POINTS': 2,
        'DRAW_POINTS': 1,
        'DISPLAY_NEGATIVE_POINTS': True,
    }
    , 
    '3p': {
        'WIN_POINTS': 3,
        'DRAW_POINTS': 1,
        'DISPLAY_NEGATIVE_POINTS': False,
    }
}

DEFAULT_TIE_BREAK_RULES = ['POINTS','GOAL_DIFFERENCE', 'GOALS', 'AWAY_GOALS']

TIE_BREAK_RULES = {
    'POINTS': {
        'field': ['points'],
        'descending': True,
        'head2head': False,
    },
    'GOAL_DIFFERENCE': {
        'field': ['goalDifference'],
        'descending': True,
        'head2head': False,
    },
    'GOALS': {
        'field': ['goals'],
        'descending': True,
        'head2head': False,
    },
    'WINS': {
        'field': ['wins'],
        'descending': True,
        'head2head': False,
    },
    'POINTS_H2H': {
        'field': ['points'],
        'descending': True,
        'head2head': True,
    },
    'GOAL_DIFFERENCE_H2H': {
        'field': ['goalDifference'],
        'descending': True,
        'head2head': True,
    },
    'GOALS_H2H': {
        'field': ['goals'],
        'descending': True,
        'head2head': True,
    },
    'AWAY_GOALS': {
        'field': ['away','goals'],
        'descending': True,
        'head2head': False,
    },
    'AWAY_GOALS_H2H': {
        'field': ['away','goals'],
        'descending': True,
        'head2head': True,
    },
}

COMPETITION_DATA = {
    'BL1': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'AWAY_GOALS_H2H',
            'AWAY_GOALS',
        ],
    },
    'BL2': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'AWAY_GOALS_H2H',
            'AWAY_GOALS',
        ],
    },
    'BL3': {
        'point_rules': [
            {
                'season_from': 2008,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'AWAY_GOALS_H2H',
            'AWAY_GOALS',
        ],
    },
    'PL': {
        'point_rules': [
            {
                'season_from': 1992,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'ELC': {
        'point_rules': [
            {
                'season_from': 2004,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'EL1': {
        'point_rules': [
            {
                'season_from': 2004,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'SA': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'SB': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'FL1': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'FL2': {
        'point_rules': [
            {
                'season_to': 1993,
                'rule': '2p',
            },
            {
                'season_from': 1994,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'PD': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOALS_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
    'SD': {
        'point_rules': [
            {
                'season_to': 1994,
                'rule': '2p',
            },
            {
                'season_from': 1995,
                'rule': '3p',
            }
        ],
        'tie_break_rules': [
            'POINTS',
            'POINTS_H2H',
            'GOAL_DIFFERENCE_H2H',
            'GOALS_H2H',
            'GOAL_DIFFERENCE',
            'GOALS',
        ],
    },
}