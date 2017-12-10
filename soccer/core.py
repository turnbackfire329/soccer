""" Central class for the soccer data api. """
import time
import datetime

from .data_connectors import FDOConnector, TMConnector
from .writers import BasicWriter, HTMLWriter, JSONWriter, BootstrapWriter
from .exceptions import NoDataConnectorException, SoccerDBNotFoundException
from .util import get_current_season, get_season_range, SORT_OPTIONS

class Soccer(object):
    """
    Central class for the soccer data api.
    """

    def __init__(self, fdo_apikey=None, mongo_settings=None, writer='basic'):
        self.dc = None
        self.season = get_current_season()
        self._create_data_connectors(fdo_apikey=fdo_apikey, mongo_settings=mongo_settings)
        self._get_writer(writer)

    def _create_data_connectors(self, fdo_apikey=None, mongo_settings=None):
        if fdo_apikey is not None:
            self.dc = FDOConnector(fdo_apikey)
        elif mongo_settings is not None:
            try:
                self.dc = TMConnector(mongo_settings)
            except SoccerDBNotFoundException:
                pass
        else:
            self.dc = FDOConnector()   

    def _get_writer(self, writer):
        if writer == 'basic':
            self.writer = BasicWriter()
        elif writer == 'json':
            self.writer = JSONWriter()
        elif writer == 'html':
            self.writer = HTMLWriter()
        elif writer == 'bootstrap':
            self.writer = BootstrapWriter()
        else:
            self.writer = BasicWriter()

    def get_fixtures(self, league_code=None, teams=None, startDate=None, endDate=None, future=None, count=None):
        if league_code is not None or teams is not None:      
            if startDate is not None and endDate is not None:
                return self.get_fixtures_by_date(league_code, teams, startDate, endDate)

            if future in (True,False) and count is not None:
                return self.get_fixtures_by_count(league_code,teams, future, count)
        else:
            return []

    def get_fixtures_by_date(self, league_code, teams, startDate, endDate):
        # get season from the date range
        fixtures = []
        seasons = get_season_range(startDate, endDate)
        for season in seasons:
            fixtures_season = self.dc.get_fixtures_by_league_code(league_code, season)
            for fixture in fixtures_season:
                fixture = self.dc.enrich_fixture(fixture)

                if teams is None or fixture["homeTeam"]["team_id"] in teams or fixture["awayTeam"]["team_id"] in teams:
                    if startDate <= fixture["dateObject"] and endDate >= fixture["dateObject"]:
                        fixtures.append(fixture)
        return fixtures

    def get_fixtures_by_count(self, league_code, teams, future, count):
        if teams is None:
            return

        fixtures = {}
        season = self.season
        date = datetime.datetime.now()
        stop_search = False
        while not stop_search:
            fixtures_season = self.dc.get_fixtures_by_league_code(league_code, season)
            fixtures_season = self.dc.sort_fixtures(fixtures_season, future)

            for fixture in fixtures_season:
                fixture = self.dc.enrich_fixture(fixture)
                if (future and fixture["dateObject"] > date ) or ( not future and fixture["dateObject"] < date):
                    # TODO: add fixture to team array
                    # team = []
                    pass
                else:
                    # TODO: add exception
                    pass

    def get_table(self, league_code, teams=None, timeFrame=None):
        return self.writer.league_table(self.dc.get_table(league_code=league_code, teams=teams, timeFrame=timeFrame))

    def get_league_table(self, league_code, season=None, matchday=None, sortBy=None, ascending=None, home=True, away=True, teams=None, head2headOnly=False):
        # sanity checks
        if sortBy is None:
            sortBy = (SORT_OPTIONS["POINTS"], SORT_OPTIONS["DIFFERENCE"], SORT_OPTIONS["GOALS"])

        if ascending is None:
            ascending = (-1, -1, -1)

        if season is None:
            season = self.season

        if not home and not away:
            return {}

        if self.dc is None:
            raise NoDataConnectorException(f'There is no data connector for {season}', season)

        if teams is None:
            # standard case: just load the table
            standings = self.dc.get_league_table_by_league_code(league_code, season, matchday)

        else:
            # load fixtures and compute table
            fixtures = self.dc.get_fixtures_by_league_code(league_code, season)

            standings = {
                "standing": self.dc.compute_team_standings(fixtures, teams=teams, home=home, away=away, head2headOnly=head2headOnly)
            }

        if home and not away:
            standings = self.dc.convert_league_table(standings)
        elif not home and away:
            standings = self.dc.convert_league_table(standings, home=False)
        standings["standing"] = self.dc.sort_league_table(standings["standing"], sortBy, ascending)
        return standings
