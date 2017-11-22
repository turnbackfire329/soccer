""" Central class for the soccer data api. """
import time
import datetime

from soccer.data_connectors import FDOConnector, TMConnector
from soccer.writers import BasicWriter
from soccer.exceptions import NoDataConnectorException, SoccerDBNotFoundException

class Soccer(object):
    """
    Central class for the soccer data api.
    """

    SORT_OPTIONS = {
        "POINTS": "points",
        "GOALS": "goals",
        "GOALS_AGAINST": "goalsAgainst",
        "DIFFERENCE": "goalDifference"
    }

    def __init__(self, fdo_apikey=None, mongo_settings=None):
        self.season = self._get_current_season()
        self._create_data_connectors(fdo_apikey=fdo_apikey, mongo_settings=mongo_settings)

    def _create_data_connectors(self, fdo_apikey=None, mongo_settings=None):
        self.dc = []

        if fdo_apikey is not None:
            fdo = FDOConnector(fdo_apikey)
            self.dc.append({
                "seasons": [self.season, self.season-1],
                "dc": fdo
            })
        else:
            fdo = FDOConnector()
            self.dc.append({
                "seasons": [self.season, self.season-1],
                "dc": fdo
            })

        if mongo_settings is not None:
            try:
                tm = TMConnector(mongo_settings)
                self.dc.append({
                    "seasons": list(range(1900, self.season)),
                    "dc": tm
                })
            except SoccerDBNotFoundException:
                pass    

    def _get_current_season(self):
        return self._get_season_from_date(datetime.date.today())

    def _get_season_from_date(self, date):
        if date.month < 8:
            return date.year - 1
        else:
            return date.year

    def _get_season_range(self, startDate, endDate):
        return list(range(self._get_season_from_date(startDate), self._get_season_from_date(endDate) + 1))

    def _get_dc(self, season):
        for data_connector in self.dc:
            print(data_connector["seasons"])
            if int(season) in data_connector["seasons"]:
                return data_connector["dc"]

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
        seasons = self._get_season_range(startDate, endDate)
        for season in seasons:
            dc = self._get_dc(season)
            fixtures_season = dc.get_fixtures_by_league_code(league_code, season)
            for fixture in fixtures_season:
                fixture = dc.enrich_fixture(fixture)

                if teams is None or fixture["homeTeamId"] in teams or fixture["awayTeamId"] in teams:
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
            dc = self._get_dc(season)
            fixtures_season = dc.get_fixtures_by_league_code(league_code, season)
            fixtures_season = dc.sort_fixtures(fixtures_season, future)

            for fixture in fixtures_season:
                fixture = dc.enrich_fixture(fixture)
                if (future and fixture["dateObject"] > date ) or ( not future and fixture["dateObject"] < date):
                    # TODO: add fixture to team array
                    # team = []
                    pass
                else:
                    # TODO: add exception
                    pass

    def get_league_table(self, league_code, season=None, matchday=None, sortBy=None, ascending=None, home=True, away=True, teams=None, head2headOnly=False):
        # sanity checks
        if sortBy is None:
            sortBy = (Soccer.SORT_OPTIONS["POINTS"], Soccer.SORT_OPTIONS["DIFFERENCE"], Soccer.SORT_OPTIONS["GOALS"])

        if ascending is None:
            ascending = (-1, -1, -1)

        if season is None:
            season = self.season

        if not home and not away:
            return {}

        dc = self._get_dc(season)

        if dc is None:
            raise NoDataConnectorException(f'There is no data connector for {season}', season)

        if teams is None:
            # standard case: just load the table
            standings = dc.get_league_table_by_league_code(league_code, season, matchday)

        else:
            # load fixtures and compute table
            fixtures = dc.get_fixtures_by_league_code(league_code, season)

            standings = {
                "standing": dc.compute_team_standings(fixtures, teams=teams, home=home, away=away, head2headOnly=head2headOnly)
            }

        if home and not away:
            standings = dc.convert_league_table(standings)
        elif not home and away:
            standings = dc.convert_league_table(standings, home=False)
        standings["standing"] = dc.sort_league_table(standings["standing"], sortBy, ascending)
        return standings
