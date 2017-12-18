""" JSON writer """
import logging
from soccer.writers import BasicWriter

class JSONWriter(BasicWriter):
    """
    JSON writer
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def league_table(self, table):
        return table

    def rank_table(self, table, position):
        return table

    def title_table(self, title_table):
        return title_table

    def fixture_list(self, fixtures):
        return fixtures