"""
SQLite Connector for soccer data. This connector
expects the european soccer dataset that can be found here:
https://www.kaggle.com/hugomathien/soccer
"""
import os
import sqlite3

from .data_connector import DataConnector
from soccer.exceptions import SoccerDBNotFoundException

class SQLiteConnector(DataConnector):
    """
    SQLite Connector for soccer data. This connector
    expects the european soccer dataset that can be found here:
    https://www.kaggle.com/hugomathien/soccer
    """
    def __init__(self, db_path):
        DataConnector.__init__(self)
        if os.path.isfile(db_path):
            self.db = sqlite3.connect(db_path)
        else:
            raise SoccerDBNotFoundException(f'The soccer database could not be found at {db_path}')

    def get_league_table(self, competitionData, matchday):
        pass

    def get_league_table_by_league_code(self, league_code, season, matchday):
        pass
    
    def get_fixtures(self, competitionData):
        pass

    def get_fixtures_by_league_code(self, league_code, season):
        pass

    def get_team(self, team_id):
        pass