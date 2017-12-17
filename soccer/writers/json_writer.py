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