""" Basic writer """

import logging

class BasicWriter(object):
    """
    Basic writer
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def league_table(self, table):
        print("    %-25s %2s %2s %2s %2s %7s %3s" % ("Team", "P", "W", "D", "L", "Goals","Pts"))
        for team in table["standings"]:
            print("%2s. %-25s %2s %2s %2s %2s %3s:%-3s %3s" % (team["position"], team["teamName"], team["playedGames"], team["wins"], team["draws"], team["losses"], team["goals"], team["goalsAgainst"], team["points"]))

    def rank_table(self, table, rank=None, teams=None):
        print("    %-25s %2s %2s %2s %2s %7s %3s" % ("Team", "P", "W", "D", "L", "Goals","Pts"))
        for team in table["standings"]:
            print("%2s. %-25s %2s %2s %2s %2s %3s:%-3s %3s" % (team["position"], team["teamName"], team["playedGames"], team["wins"], team["draws"], team["losses"], team["goals"], team["goalsAgainst"], team["points"]))

    def title_table(self, title_table):
        print(title_table)

    def fixture_list(self, fixtures):
        if fixtures is None:
            print("No fixtures found")
        print(fixtures)   

    def ranks_of_teams(self, ranks_of_teams):
        pass

    def rank_and_titles(self, rank_table, ranks_of_teams, teams=None):
        pass
