"""
This connector loads data from the football-data.org service.
It uses the footballdataorg package to load the data.
"""
import datetime
from footballdataorg.fd import FD
from .data_connector import DataConnector

class FDOConnector(DataConnector):
    """
    This connector loads data from the football-data.org service.
    It uses the footballdataorg package to load the data.
    """
    def __init__(self, fd_apikey=None):
        DataConnector.__init__(self)
        self.fdo = FD(fd_apikey)

    def get_league_table(self, competitionData, matchday):
        return self.fdo.get_league_table(competitionData, matchday)

    def get_league_table_by_league_code(self, league_code, season, matchday):
        competitionData = self.fdo.get_competition(league_code=league_code, season=season)
        return self.get_league_table(competitionData, matchday)
    
    def get_fixtures(self, competitionData):
        return self.fdo.get_fixtures(competitionData)['fixtures']

    def get_fixtures_by_league_code(self, league_code, season):
        competitionData = self.fdo.get_competition(league_code=league_code, season=season)
        return self.get_fixtures(competitionData)

    def get_team(self, team_id):
        return self.fdo.get_team(team_id)

    def enrich_fixture(self, fixture):
        fixture = super(FDOConnector, self).enrich_fixture(fixture)

        homeId = int(fixture["_links"]["homeTeam"]["href"].split('/')[5])
        awayId = int(fixture["_links"]["awayTeam"]["href"].split('/')[5])

        fixture["homeTeam"] = {
            "team_id": homeId
        }
        fixture["awayTeam"] = {
            "team_id": awayId
        }

        fixture["dateObject"] = datetime.datetime.strptime(fixture["date"], '%Y-%m-%dT%H:%M:%SZ')
        return fixture