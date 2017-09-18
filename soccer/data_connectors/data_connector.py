""" Basic connector that offers the soccer data interface """

class DataConnector(object):
    """
    Basic connector that offers the soccer data interface
    """
    def __init__(self):
        pass

    def get_league_table(self, competitionData, matchday):
        pass

    def get_league_table_by_league_code(self, league_code, season, matchday):
        pass
    
    def get_fixtures(self, competitionData):
        pass

    def get_fixtures_by_league_code(self, league_code, season):
        pass

    def get_team(self, team_id):
        pass

    def convert_league_table(self, standings, home=True):
        for standing in standings["standing"]:
            if home:
                standing["goals"] = standing["home"]["goals"]
                standing["goalsAgainst"] = standing["home"]["goalsAgainst"]
                standing["wins"] = standing["home"]["wins"]
                standing["draws"] = standing["home"]["draws"]
                standing["losses"] = standing["home"]["losses"]
            else:
                standing["goals"] = standing["away"]["goals"]
                standing["goalsAgainst"] = standing["away"]["goalsAgainst"]
                standing["wins"] = standing["away"]["wins"]
                standing["draws"] = standing["away"]["draws"]
                standing["losses"] = standing["away"]["losses"]

            standing["goalDifference"] = standing["goals"] - standing["goalsAgainst"]
            standing["playedGames"] = standing["wins"] + standing["draws"] + standing["losses"]
            standing["points"] = standing["wins"] * 3 + standing["draws"]
        return standings

    def sort_league_table(self, standings, sortBy=None, ascending=None):
        if sortBy is None:
            sortBy = (Soccer.SORT_OPTIONS["POINTS"], Soccer.SORT_OPTIONS["DIFFERENCE"], Soccer.SORT_OPTIONS["GOALS"])

        if ascending is None:
            ascending = (-1, -1, -1)

        def getSortTuple(x, sortBy, ascending):
            t = ()
            for i in range(0, len(sortBy)):
                t = t + (ascending[i] * x[sortBy[i]],)
            return t

        standings = sorted(standings, key=lambda x: getSortTuple(x, sortBy, ascending))

        for position in range(0, len(standings)):
            standings[position]["position"] = position + 1
        return standings

    def enrich_fixture(self, fixture):
        if fixture["result"]["goalsHomeTeam"] == fixture["result"]["goalsAwayTeam"]:
            fixture["result"]["pointsHomeTeam"] = 1
            fixture["result"]["winsHomeTeam"] = 0
            fixture["result"]["drawsHomeTeam"] = 1
            fixture["result"]["lossesHomeTeam"] = 0
            fixture["result"]["pointsAwayTeam"] = 1
            fixture["result"]["winsAwayTeam"] = 0
            fixture["result"]["drawsAwayTeam"] = 1
            fixture["result"]["lossesAwayTeam"] = 0
        elif fixture["result"]["goalsHomeTeam"] > fixture["result"]["goalsAwayTeam"]:
            fixture["result"]["pointsHomeTeam"] = 3
            fixture["result"]["winsHomeTeam"] = 1
            fixture["result"]["drawsHomeTeam"] = 0
            fixture["result"]["lossesHomeTeam"] = 0
            fixture["result"]["pointsAwayTeam"] = 0
            fixture["result"]["winsAwayTeam"] = 0
            fixture["result"]["drawsAwayTeam"] = 0
            fixture["result"]["lossesAwayTeam"] = 1
        else:
            fixture["result"]["pointsHomeTeam"] = 0
            fixture["result"]["winsHomeTeam"] = 0
            fixture["result"]["drawsHomeTeam"] = 0
            fixture["result"]["lossesHomeTeam"] = 1
            fixture["result"]["pointsAwayTeam"] = 3
            fixture["result"]["winsAwayTeam"] = 1
            fixture["result"]["drawsAwayTeam"] = 0
            fixture["result"]["lossesAwayTeam"] = 0
        return fixture

    def compute_team_standings(self, fixtures, teams, home=True, away=True, head2headOnly=False):
        teamStandings = {}
        for team in teams:
            teamData = self.get_team(team)

            teamStandings[team] = {
                "teamName": teamData["name"],
                "goals": 0,
                "goalsAgainst": 0,
                "points": 0,
                "playedGames":0,
                "wins":0,
                "draws":0,
                "losses":0,
                "goalsDifference":0,
                "home": {
                    "goals": 0,
                    "goalsAgainst": 0,
                    "wins":0,
                    "draws":0,
                    "losses":0
                },
                "away": {
                    "goals": 0,
                    "goalsAgainst": 0,
                    "wins":0,
                    "draws":0,
                    "losses":0
                }
            }

        for fixture in fixtures["fixtures"]:

            if fixture["status"] == "FINISHED":
                fixture = self.enrich_fixture(fixture)
                homeId = int(fixture["_links"]["homeTeam"]["href"].split('/')[5])
                awayId = int(fixture["_links"]["awayTeam"]["href"].split('/')[5])

                if home and homeId in teams and (not head2headOnly or awayId in teams):
                    teamStandings[homeId]["home"]["goals"] =        teamStandings[homeId]["home"]["goals"] + fixture["result"]["goalsHomeTeam"]
                    teamStandings[homeId]["home"]["goalsAgainst"] = teamStandings[homeId]["home"]["goalsAgainst"] + fixture["result"]["goalsAwayTeam"]
                    teamStandings[homeId]["home"]["wins"] =         teamStandings[homeId]["home"]["wins"] + fixture["result"]["winsHomeTeam"]
                    teamStandings[homeId]["home"]["draws"] =        teamStandings[homeId]["home"]["draws"] + fixture["result"]["drawsHomeTeam"]
                    teamStandings[homeId]["home"]["losses"] =       teamStandings[homeId]["home"]["losses"] + fixture["result"]["lossesHomeTeam"]
                    teamStandings[homeId]["goals"] =                teamStandings[homeId]["goals"] + fixture["result"]["goalsHomeTeam"]
                    teamStandings[homeId]["goalsAgainst"] =         teamStandings[homeId]["goalsAgainst"] + fixture["result"]["goalsAwayTeam"]
                    teamStandings[homeId]["points"] =               teamStandings[homeId]["points"] + fixture["result"]["pointsHomeTeam"]
                    teamStandings[homeId]["playedGames"] =          teamStandings[homeId]["playedGames"] + 1
                    teamStandings[homeId]["wins"] =                 teamStandings[homeId]["wins"] + fixture["result"]["winsHomeTeam"]
                    teamStandings[homeId]["draws"] =                teamStandings[homeId]["draws"] + fixture["result"]["drawsHomeTeam"]
                    teamStandings[homeId]["losses"] =               teamStandings[homeId]["losses"] + fixture["result"]["lossesHomeTeam"]
                    teamStandings[homeId]["goalDifference"] =       teamStandings[homeId]["goals"] - teamStandings[homeId]["goalsAgainst"] 
                if away and awayId in teams and (not head2headOnly or homeId in teams):
                    teamStandings[awayId]["away"]["goals"] =        teamStandings[awayId]["away"]["goals"] + fixture["result"]["goalsAwayTeam"]
                    teamStandings[awayId]["away"]["goalsAgainst"] = teamStandings[awayId]["away"]["goalsAgainst"] + fixture["result"]["goalsHomeTeam"]
                    teamStandings[awayId]["away"]["wins"] =         teamStandings[awayId]["away"]["wins"] + fixture["result"]["winsAwayTeam"]
                    teamStandings[awayId]["away"]["draws"] =        teamStandings[awayId]["away"]["draws"] + fixture["result"]["drawsAwayTeam"]
                    teamStandings[awayId]["away"]["losses"] =       teamStandings[awayId]["away"]["losses"] + fixture["result"]["lossesAwayTeam"]
                    teamStandings[awayId]["goals"] =                teamStandings[awayId]["goals"] + fixture["result"]["goalsAwayTeam"]
                    teamStandings[awayId]["goalsAgainst"] =         teamStandings[awayId]["goalsAgainst"] + fixture["result"]["goalsHomeTeam"]
                    teamStandings[awayId]["points"] =               teamStandings[awayId]["points"] + fixture["result"]["pointsAwayTeam"]
                    teamStandings[awayId]["playedGames"] =          teamStandings[awayId]["playedGames"] + 1
                    teamStandings[awayId]["wins"] =                 teamStandings[awayId]["wins"] + fixture["result"]["winsAwayTeam"]
                    teamStandings[awayId]["draws"] =                teamStandings[awayId]["draws"] + fixture["result"]["drawsAwayTeam"]
                    teamStandings[awayId]["losses"] =               teamStandings[awayId]["losses"] + fixture["result"]["lossesAwayTeam"]
                    teamStandings[awayId]["goalDifference"] =       teamStandings[awayId]["goals"] - teamStandings[awayId]["goalsAgainst"]
        return list(teamStandings.values())