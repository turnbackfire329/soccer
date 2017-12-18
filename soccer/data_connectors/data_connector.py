""" Basic connector that offers the soccer data interface """

import datetime
import logging
from ..util import get_current_season, get_empty_team_standings, SORT_OPTIONS


class DataConnector(object):
    """
    Basic connector that offers the soccer data interface
    """

    TIME_FRAME_TYPES = ("date", "season", "matchday")
    TABLE_STATUS = {
        'done': 'done',
        'pending': 'pending',
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

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
            sortBy = (SORT_OPTIONS["POINTS"], SORT_OPTIONS["DIFFERENCE"], SORT_OPTIONS["GOALS"])

        if ascending is None:
            ascending = (-1, -1, -1)

        def getSortTuple(x, sortBy, ascending):
            t = ()
            for i in range(0, len(sortBy)):
                t = t + (ascending[i] * x[sortBy[i]],)
            return t

        standings.sort(key=lambda x: getSortTuple(x, sortBy, ascending))

        for position in range(0, len(standings)):
            standings[position]["position"] = position + 1
        return standings

    def sort_fixtures(self, fixtures, ascending=True):
        if ascending:
            fixtures.sort(key=lambda x: (x["dateObject"]))
        else:
            fixtures.sort(key=lambda x: (-x["dateObject"]))
        return fixtures

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

        if teams is not None:
            for team in teams:
                teamStandings[team] = get_empty_team_standings()
                teamData = self.get_team(team)
                teamStandings[team]["teamName"] = teamData["name"]

        for fixture in fixtures:
            fixture = self.enrich_fixture(fixture)
            if fixture["dateObject"] < datetime.datetime.now() and fixture["result"]["goalsHomeTeam"] != "-":
                homeId = fixture["homeTeam"]["team_id"]
                awayId = fixture["awayTeam"]["team_id"]

                if teams is None or (home and homeId in teams and (not head2headOnly or awayId in teams)):
                    if homeId not in teamStandings:
                        teamStandings[homeId] = get_empty_team_standings()
                        teamData = self.get_team(homeId)
                        teamStandings[homeId]["teamName"] = teamData["name"]

                    teamStandings[homeId]["home"]["goals"] =        teamStandings[homeId]["home"]["goals"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[homeId]["home"]["goalsAgainst"] = teamStandings[homeId]["home"]["goalsAgainst"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[homeId]["home"]["wins"] =         teamStandings[homeId]["home"]["wins"] + int(fixture["result"]["winsHomeTeam"])
                    teamStandings[homeId]["home"]["draws"] =        teamStandings[homeId]["home"]["draws"] + int(fixture["result"]["drawsHomeTeam"])
                    teamStandings[homeId]["home"]["losses"] =       teamStandings[homeId]["home"]["losses"] + int(fixture["result"]["lossesHomeTeam"])
                    teamStandings[homeId]["goals"] =                teamStandings[homeId]["goals"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[homeId]["goalsAgainst"] =         teamStandings[homeId]["goalsAgainst"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[homeId]["points"] =               teamStandings[homeId]["points"] + int(fixture["result"]["pointsHomeTeam"])
                    teamStandings[homeId]["playedGames"] =          teamStandings[homeId]["playedGames"] + 1
                    teamStandings[homeId]["wins"] =                 teamStandings[homeId]["wins"] + int(fixture["result"]["winsHomeTeam"])
                    teamStandings[homeId]["draws"] =                teamStandings[homeId]["draws"] + int(fixture["result"]["drawsHomeTeam"])
                    teamStandings[homeId]["losses"] =               teamStandings[homeId]["losses"] + int(fixture["result"]["lossesHomeTeam"])
                    teamStandings[homeId]["goalDifference"] =       teamStandings[homeId]["goals"] - teamStandings[homeId]["goalsAgainst"] 

                if teams is None or ( away and awayId in teams and (not head2headOnly or homeId in teams)):
                    if awayId not in teamStandings:
                        teamStandings[awayId] = get_empty_team_standings()
                        teamData = self.get_team(awayId)
                        teamStandings[awayId]["teamName"] = teamData["name"]
                        
                    teamStandings[awayId]["away"]["goals"] =        teamStandings[awayId]["away"]["goals"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[awayId]["away"]["goalsAgainst"] = teamStandings[awayId]["away"]["goalsAgainst"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[awayId]["away"]["wins"] =         teamStandings[awayId]["away"]["wins"] + int(fixture["result"]["winsAwayTeam"])
                    teamStandings[awayId]["away"]["draws"] =        teamStandings[awayId]["away"]["draws"] + int(fixture["result"]["drawsAwayTeam"])
                    teamStandings[awayId]["away"]["losses"] =       teamStandings[awayId]["away"]["losses"] + int(fixture["result"]["lossesAwayTeam"])
                    teamStandings[awayId]["goals"] =                teamStandings[awayId]["goals"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[awayId]["goalsAgainst"] =         teamStandings[awayId]["goalsAgainst"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[awayId]["points"] =               teamStandings[awayId]["points"] + int(fixture["result"]["pointsAwayTeam"])
                    teamStandings[awayId]["playedGames"] =          teamStandings[awayId]["playedGames"] + 1
                    teamStandings[awayId]["wins"] =                 teamStandings[awayId]["wins"] + int(fixture["result"]["winsAwayTeam"])
                    teamStandings[awayId]["draws"] =                teamStandings[awayId]["draws"] + int(fixture["result"]["drawsAwayTeam"])
                    teamStandings[awayId]["losses"] =               teamStandings[awayId]["losses"] + int(fixture["result"]["lossesAwayTeam"])
                    teamStandings[awayId]["goalDifference"] =       teamStandings[awayId]["goals"] - teamStandings[awayId]["goalsAgainst"]
        return list(teamStandings.values())

    def _get_seasons_from_timeframe(self, timeFrame):
        timeFrame = self._check_timeFrame(timeFrame)

        if timeFrame["type"] == 'season' or timeFrame["type"] == 'matchday':
            return range(timeFrame['season_from'], timeFrame['season_to'] + 1)
        else:
            return range(timeFrame['date_from'].year, timeFrame['date_to'].year + 1)

    def _check_timeFrame(self, timeFrame=None):
        bValid = False

        if timeFrame is None:
            current_season = str(get_current_season())
            timeFrame = {
                "type": "season",
                "season_from": current_season,
                "season_to": current_season
            }
            bValid = True
        elif "type" in timeFrame:
            timeFrameType = timeFrame["type"]

            if timeFrameType in self.TIME_FRAME_TYPES:
                if timeFrameType == "date":
                    if "date_from" in timeFrame and "date_to" in timeFrame:
                        bValid = True
                elif timeFrameType == "season":
                    if "season_from" in timeFrame and "season_to" in timeFrame:
                        bValid = True
                elif timeFrameType == "matchday":
                    if "season_from" in timeFrame and "season_to" in timeFrame and "matchday_from" in timeFrame and "matchday_to" in timeFrame:
                        bValid = True
        
        if bValid == False:
            raise InvalidTimeFrameException(f"Invalid time frame given: {timeFrame}", timeFrame)
        else:
            return timeFrame