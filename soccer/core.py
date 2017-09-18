""" Central class for the soccer data api. """
import time

from soccer.data_connectors import FDOConnector, SQLiteConnector
from soccer.writers import Writer
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

    def __init__(self, fdo_apikey=None, db_path=None):
        self.season = self._get_current_season()
        self._create_data_connectors(fdo_apikey=fdo_apikey, db_path=db_path)

    def _create_data_connectors(self, fdo_apikey=None, db_path=None):
        self.dc = []
        fdo = FDOConnector(fdo_apikey)
        self.dc.append({
            "seasons": [self.season, self.season-1],
            "dc": fdo
        })

        if db_path is not None:
            try:
                db = SQLiteConnector(db_path)
                self.dc.append({
                    "seasons": list(range(2008, self.season-1)),
                    "dc": db
                })
            except SoccerDBNotFoundException:
                pass    

    def _get_current_season(self):
        month = int(time.strftime("%m"))
        year = int(time.strftime("%Y"))
        if month < 8:
            return year - 1
        else:
            return year

    def _get_dc(self, season):
        for data_connector in self.dc:
            print(data_connector["seasons"])
            if int(season) in data_connector["seasons"]:
                return data_connector["dc"]

    def get_league_table(self, competition, season=None, matchday=None, sortBy=None, ascending=None, home=True, away=True, teams=None, head2headOnly=False):
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
            standings = dc.get_league_table_by_league_code(competition, season, matchday)

        else:
            # load fixtures and compute table
            fixtures = dc.get_fixtures_by_league_code(competition, season)

            standings = {
                "standing": dc.compute_team_standings(fixtures, teams=teams, home=home, away=away, head2headOnly=head2headOnly)
            }

        if home and not away:
            standings = dc.convert_league_table(standings)
        elif not home and away:
            standings = dc.convert_league_table(standings, home=False)
        standings["standing"] = dc.sort_league_table(standings["standing"], sortBy, ascending)
        return standings
