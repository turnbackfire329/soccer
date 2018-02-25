""" Central class for the soccer data api. """
import time
import datetime
import logging

from .data_connectors import FDOConnector, TMConnector
from .writers import BasicWriter, HTMLWriter, JSONWriter, BootstrapWriter
from .exceptions import NoDataConnectorException, SoccerDBNotFoundException
from .util import get_settings, get_current_season, get_season_range, SORT_OPTIONS

class Soccer(object):
    """
    Central class for the soccer data api.
    """

    def __init__(self, config_path=None, fdo_apikey=None, writer='basic'):
        self.logger = logging.getLogger(__name__)
        self.dc = None
        if config_path is None:
            config_path = "soccer.cfg"

        self.season = get_current_season()
        self.settings = get_settings(config_path)
        self.logger.debug(f"Loaded Settings: {self.settings}")
        self._create_data_connectors(fdo_apikey=fdo_apikey, mongo_settings=self.settings)
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

    def get_table(self, league_code, teams=None, timeFrame=None, rank=None):
        if (rank is None and teams is None) or (rank is not None and teams is not None):
            return self.writer.league_table(self.dc.get_table(league_code=league_code, teams=teams, timeFrame=timeFrame))
        else:
            seasons = self.dc._get_seasons_from_timeframe(timeFrame)

            if len(seasons) == 1:
                return self.writer.rank_table(self.dc.get_table(league_code=league_code, teams=teams, timeFrame=timeFrame), rank=rank, teams=teams)
            else: 
                if rank is not None:
                    return self.writer.title_table_and_rank_table(
                        title_table=self.dc.get_title_table(league_code=league_code, timeFrame=timeFrame, rank=rank), 
                        rank_table=self.dc.get_table(league_code=league_code, teams=teams, timeFrame=timeFrame),
                        rank=rank,
                        )
                else:
                    return self.writer.rank_and_titles(
                        rank_table=self.dc.get_table(league_code=league_code, teams=teams, timeFrame=timeFrame),
                        ranks_of_teams=self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeFrame=timeFrame), 
                        teams=teams)

    def get_fixtures(self, league_code=None, teams=None, timeFrame=None, count=None, future=None, home=True, away=True):
        return self.writer.fixture_list(self.dc.get_fixtures(league_code=league_code, teams=teams, timeFrame=timeFrame, count=count, future=future, home=home, away=away))

    def get_current_matchday(self, competition):
        return self.dc.get_current_matchday(competition)
    
    def get_titles(self, league_code, teams=None, timeFrame=None, rank=None):
        if teams is None:
            return self.writer.title_table(self.dc.get_title_table(league_code=league_code, teams=teams, timeFrame=timeFrame, rank=rank))
        else:
            return self.writer.ranks_teams(self.dc.get_ranks_of_teams(league_code=league_code, teams=teams, timeFrame=timeFrame))

    def get_goal_table(self, league_code=None, players=None, timeFrame=None):
        return self.writer.goal_table(self.dc.get_scorer_table(league_code=league_code, players=players, timeFrame=timeFrame, goals=True))

    def get_assist_table(self, league_code=None, players=None, timeFrame=None):
        return self.writer.assist_table(self.dc.get_scorer_table(league_code=league_code, players=players, timeFrame=timeFrame, assists=True))
    
    def get_scorer_table(self, league_code=None, players=None, timeFrame=None):
        return self.writer.scorer_table(self.dc.get_scorer_table(league_code=league_code, players=players, timeFrame=timeFrame, goals=True, assists=True))

    def search_team(self, query):
        return self.dc.search_team(query)
    
    def search_player(self, query):
        return self.dc.search_player(query)
