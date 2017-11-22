"""
This connector loads data from the transfermarkt.com database that is created via the scrapy project
that is part of this package
"""

from urllib.parse import quote_plus
from pymongo import MongoClient
from .data_connector import DataConnector

class TMConnector(DataConnector):
    """
    This connector loads data from the mongodb that stores the transfermarkt.com data
    """
    def __init__(self, mongo_settings=None):
        DataConnector.__init__(self)
        if mongo_settings is not None:
            uri = "mongodb://%s:%s@%s:%s" % (
                quote_plus(mongo_settings['MONGODB_USER']), quote_plus(mongo_settings['MONGODB_PASSWORD']), mongo_settings['MONGODB_SERVER'], mongo_settings['MONGODB_PORT'])

            self.mdb = MongoClient(uri, authSource=mongo_settings['MONGODB_AUTH_DB'])

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