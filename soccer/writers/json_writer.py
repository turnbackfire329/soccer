""" JSON writer """
from soccer.writers import BasicWriter

class JSONWriter(BasicWriter):
    """
    JSON writer
    """
    def __init__(self):
        pass

    def league_table(self, table):
        return table