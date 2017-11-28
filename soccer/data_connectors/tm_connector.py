"""
This connector loads data from the transfermarkt.com database that is created via the scrapy project
that is part of this package
"""
import datetime
from urllib.parse import quote_plus
from pymongo import MongoClient
from .data_connector import DataConnector
from ..exceptions import InvalidTimeFrameException
from ..util import get_current_season

TIME_FRAME_TYPES = ("date", "season", "matchday")

class TMConnector(DataConnector):
    """
    This connector loads data from the mongodb that stores the transfermarkt.com data
    """
    def __init__(self, mongo_settings=None):
        DataConnector.__init__(self)
        if mongo_settings is not None:
            uri = "mongodb://%s:%s@%s:%s" % (
                quote_plus(mongo_settings['MONGODB_USER']), quote_plus(mongo_settings['MONGODB_PASSWORD']), mongo_settings['MONGODB_SERVER'], mongo_settings['MONGODB_PORT'])

            self.mdb = MongoClient(uri, authSource=mongo_settings['MONGODB_AUTH_DB'])
            self.db = self.mdb[mongo_settings['MONGODB_DB']]
            self.collections = {
                "teams": self.db["teams"],
                "team_season": self.db["team_season"],
                "competitions": self.db["competitions"],
                "competition_season": self.db["competition_season"],
                "players": self.db["players"],
                "fixtures": self.db["fixtures"],
                "tables": self.db["tables"]
            }

    def get_league_table(self, competitionData, matchday):
        pass

    def get_league_table_by_league_code(self, league_code, season, matchday):
        pass
    
    def get_fixtures(self, competitionData):
        pass

    def get_fixtures_by_league_code(self, league_code, season):
        pass

    def get_fixtures_by_timeFrame(self, league_code, teams=None, timeFrame=None):
        timeFrame = self._check_timeFrame(timeFrame=timeFrame)

        findDict = {
            "league_code": league_code
        }

        if teams is not None:
            findDict["$and"] = [{"$or":[{ "homeTeam.id": { "$in": teams }}, { "awayTeam.id": { "$in": teams }}]}]

        if timeFrame["type"] == "date":
            findDict["date"] = {"$and":[{ "$gte": timeFrame["date_from"] }, { "$lte": timeFrame["date_to"] }]}
        elif timeFrame["type"] == "season":
            if "$and" in findDict:
                findDict.append({'season': {'$gte': timeFrame["season_from"]}},{'season': {'$lte': timeFrame["season_to"]}})
            else: 
                findDict["$and"] = [{'season': {'$gte': timeFrame["season_from"]}},{'season': {'$lte': timeFrame["season_to"]}}]
        elif timeFrame["type"] == "matchday":
            if "$and" in findDict:
                findDict.append({'season': {'$gte': timeFrame["season_from"]}},{'season': {'$lte': timeFrame["season_to"]}})
            else: 
                findDict["$and"] = [{'season': {'$gte': timeFrame["season_from"]}},{'season': {'$lte': timeFrame["season_to"]}}]

            findMatchday = [{
                "$and": [{"season": { "$gt": timeFrame["season_from"] }}, {"season": { "$lt": timeFrame["season_to"] }}]
            },{
                "$and": [{"season": { "$eq": timeFrame["season_from"] }}, {"matchday": { "$gte": timeFrame["matchday_from"] }}]
            },{
                "$and": [{"season": { "$eq": timeFrame["season_to"] }}, {"matchday": { "$lte": timeFrame["matchday_to"] }}]
            }]

            if "$and" in findDict:
                findDict["$and"].append({"$or":findMatchday})
            else:
                findDict["$or"] = findMatchday
    
        fixtures = list(self.collections["fixtures"].find(findDict))
        return fixtures


    def get_team(self, team_id):
        return self.collections['teams'].find_one({'team_id':team_id})

    def get_table(self, league_code, teams=None, timeFrame=None):
        timeFrame = self._check_timeFrame(timeFrame)

        existingTable = self.collections["tables"].find_one({
            "league_code": league_code,
            "teams": teams,
            "timeFrame": timeFrame
        })

        if existingTable is None or (existingTable["status"] == "pending" and existingTable["next_update"] < datetime.datetime.now()):
            table_id = None
            if existingTable is not None and existingTable["status"] == "pending":
                table_id = existingTable["_id"]
            table = self.create_table(league_code, teams, timeFrame, table_id)
            return table
        else:
            return existingTable

    def create_table(self, league_code, teams=None, timeFrame=None, table_id=None):
        timeFrame = self._check_timeFrame(timeFrame)

        fixtures = self.get_fixtures_by_timeFrame(league_code, teams, timeFrame)

        table_status = "done",
        next_update = None
        for fixture in fixtures:
            fixture = self.enrich_fixture(fixture)
            if fixture["dateObject"] > datetime.datetime.now():
                table_status = "pending"
                if next_update is None or next_update > fixture["dateObject"]:
                    next_update = fixture["dateObject"]

        standings = self.compute_team_standings(fixtures, teams)
        standings = self.sort_league_table(standings)
        table = {
            "league_code": league_code,
            "teams": teams,
            "timeFrame": timeFrame,
            "standings": standings,
            "status": table_status,
            "next_update": next_update
        }

        if table_id is not None:
            self.collections["tables"].update_one({'_id': table_id}, {'$set': table})
        else:
            self.collections["tables"].insert(table)

        return table

    def enrich_fixture(self, fixture):
        fixture = super(TMConnector, self).enrich_fixture(fixture)
        if "date" in fixture:
            fixture["dateObject"] = fixture["date"]
        else:
            fixture["dateObject"] = datetime.datetime(datetime.MINYEAR, 1, 1)
        return fixture

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

            if timeFrameType in TIME_FRAME_TYPES:
                if timeFrameType == "date":
                    if "date_from" in timeFrame and "date_to" in timeFrame:
                        bValid = True
                elif timeFrameType == "season":
                    if "season_from" in timeFrame and "season_to" in timeFrame:
                        bValid = True
                elif timeFrameType == "matchday":
                    if "season_from" in timeFrame and "season_to" in timeFrame and "matchday_from" in timeFrame and "matchday_from" in timeFrame:
                        bValid = True
        
        if bValid == False:
            raise InvalidTimeFrameException(f"Invalid time frame given: {timeFrame}", timeFrame)
        else:
            return timeFrame

        