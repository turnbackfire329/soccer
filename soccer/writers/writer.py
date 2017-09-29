""" Basic writer """
class BasicWriter(object):
    """
    Basic writer
    """
    def __init__(self):
        pass

    def league_table(self, standings):
        print("    %-25s %2s %2s %2s %2s %7s %3s" % ("Team", "P", "W", "D", "L", "Goals","Pts"))
        for team in standings["standing"]:
            print("%2s. %-25s %2s %2s %2s %2s %3s:%-3s %3s" % (team["position"], team["teamName"], team["playedGames"], team["wins"], team["draws"], team["losses"], team["goals"], team["goalsAgainst"], team["points"]))