"""
This connector loads data from the football-data.org service.
It uses the footballdataorg package to load the data.
"""
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

    def get_current_season(self):
        comps = self.fdo.get_competitions()
        return comps[0]['year']
