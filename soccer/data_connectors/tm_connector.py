"""
This connector loads data from the transfermarkt.com database that is created via the scrapy project
that is part of this package
"""
import datetime
import string
from urllib.parse import quote_plus
from pymongo import MongoClient, ASCENDING, DESCENDING
from .data_connector import DataConnector
from ..exceptions import InvalidTimeFrameException
from ..util import get_current_season, make_ngrams, DEFAULT_TIE_BREAK_RULES

class TMConnector(DataConnector):
    """
    This connector loads data from the mongodb that stores the transfermarkt.com data
    """
    def __init__(self, mongo_settings=None):
        DataConnector.__init__(self)
        if mongo_settings is not None:
            uri = "mongodb://%s:%s@%s:%s" % (
                quote_plus(mongo_settings['mongodb_user']), quote_plus(mongo_settings['mongodb_password']), mongo_settings['mongodb_server'], mongo_settings['mongodb_port'])

            self.mdb = MongoClient(uri, authSource=mongo_settings['mongodb_auth_db'])
            self.db = self.mdb[mongo_settings['mongodb_db']]
            self.collections = {
                "teams": self.db["teams"],
                "team_season": self.db["team_season"],
                "teams.search": self.db["teams.search"],
                "competitions": self.db["competitions"],
                "competition_season": self.db["competition_season"],
                "players": self.db["players"],
                "players.search": self.db["players.search"],
                "fixtures": self.db["fixtures"],
                "tables": self.db["tables"]
            }
            self.logger.info(f"Mongo DB connection initialized")

    def get_fixtures(self, league_code=None, teams=None, players=None, timeFrame=None, count=None, future=None, home=True, away=True):
        if league_code is None and teams is None and players is None:
            return None

        findDict = {}
        if league_code is not None:
            findDict['league_code'] = league_code

        if teams is not None:
            team_ids = self._get_team_ids_from_teams(teams)
            findDict_team_or = []
            if home == True:
                findDict_team_or = findDict_team_or + [{ "homeTeam.team_id": { "$in": team_ids }}]
            if away == True:
                findDict_team_or = findDict_team_or + [{ "awayTeam.team_id": { "$in": team_ids }}]

            findDict["$and"] = [{"$or":findDict_team_or}]

        if players is not None:
            player_ids = self._get_player_ids_from_players(players)
            findDict_player_or = [
                                        { "goals.player_id": { "$in": player_ids }}, 
                                        { "assists.player_id": { "$in": player_ids }},
                                        { "cards.player_id": { "$in": player_ids }},
            ]
            if home == True:
                findDict_player_or = findDict_player_or + [
                                        { "lineups.home.lineup.playerid": { "$in": player_ids }},
                                        { "lineups.home.subs.in.playerid": { "$in": player_ids }},
                                        ]
            if away == True:
                findDict_player_or = findDict_player_or + [
                                        { "lineups.away.lineup.playerid": { "$in": player_ids }},
                                        { "lineups.away.subs.in.playerid": { "$in": player_ids }},
                                        ]
            findDict["$and"] = [{"$or":findDict_player_or}]

        if timeFrame is None and count is not None:
            if future is True:
                findDict["$and"].extend([
                    {"date":{ "$gte": datetime.datetime.now()}}, 
                ])
            else:
                findDict["$and"].extend([
                    {"date":{ "$lte": datetime.datetime.now()}}, 
                ])
        else:
            timeFrame = self._check_timeFrame(timeFrame=timeFrame)

            if timeFrame["type"] == "date":
                if "$and" in findDict:
                    findDict["$and"].extend([
                        {"date":{ "$gte": timeFrame["date_from"]}}, 
                        {"date":{ "$lte": timeFrame["date_to"]}},
                    ])
                else: 
                    findDict["$and"] = [{"date":{ "$gte": timeFrame["date_from"]}}, {"date":{ "$lte": timeFrame["date_to"]}}]
            elif timeFrame["type"] == "season":
                if "$and" in findDict:
                    findDict["$and"].extend([
                        {'season': {'$gte': timeFrame["season_from"]}},
                        {'season': {'$lte': timeFrame["season_to"]}}
                    ])
                else: 
                    findDict["$and"] = [{'season': {'$gte': timeFrame["season_from"]}},{'season': {'$lte': timeFrame["season_to"]}}]
            elif timeFrame["type"] == "matchday":
                if "$and" in findDict:
                    findDict["$and"].extend([
                        {'season': {'$gte': timeFrame["season_from"]}},
                        {'season': {'$lte': timeFrame["season_to"]}},
                    ])
                else: 
                    findDict["$and"] = [{'season': {'$gte': timeFrame["season_from"]}},{'season': {'$lte': timeFrame["season_to"]}}]

                if timeFrame["season_from"] != timeFrame["season_to"]:
                    findMatchday = [{
                        "$and": [{"season": { "$gt": timeFrame["season_from"]}}, {"season": { "$lt": timeFrame["season_to"]}}]
                    },{
                        "$and": [{"season": { "$eq": timeFrame["season_from"]}}, {"matchday": { "$gte": timeFrame["matchday_from"]}}]
                    },{
                        "$and": [{"season": { "$eq": timeFrame["season_to"]}}, {"matchday": { "$lte": timeFrame["matchday_to"]}}]
                    }]
                    findDict["$and"].append({"$or":findMatchday})
                else:
                    findDict["$and"].extend([
                        {"matchday": { "$lte": timeFrame["matchday_to"]}},
                        {"matchday": { "$gte": timeFrame["matchday_from"]}},
                    ])

        self.logger.debug(f"Looking for fixtures with the following findDict: {findDict}") 

        if count is None:
            count = 0

        if future is None or future is True:
            fixtures = list(self.collections["fixtures"].find(findDict).sort('date', ASCENDING).limit(count))
        else:
            fixtures = list(self.collections["fixtures"].find(findDict).sort('date', DESCENDING).limit(count))

        return fixtures

    def get_team(self, team_id):
        return self.collections['teams'].find_one({'team_id':team_id})

    def get_player(self, player_id):
        return self.collections['players'].find_one({'player_id':player_id})

    def get_table(self, league_code, teams=None, timeFrame=None):
        timeFrame = self._check_timeFrame(timeFrame)

        if teams is not None:
            self.logger.debug(f"The following teams are given: {teams}")
            if len(teams) == 1:
                self.logger.debug(f"Since only one team was given the complete table is calculated")
                teams = None

        findDict = {
            "league_code": league_code,
            "teams": teams,
            "timeFrame": timeFrame
        }
        self.logger.debug(f"Looking for a table with the following findDict: {findDict}")  

        existingTable = self.collections["tables"].find_one({
            "league_code": league_code,
            "teams": teams,
            "timeFrame": timeFrame
        })

        if existingTable is None or (existingTable["status"] == self.TABLE_STATUS['pending'] and existingTable["next_update"] < datetime.datetime.now()):
            table_id = None
            self.logger.debug(f"Table needs to be created") 
            if existingTable is not None and existingTable["status"] == self.TABLE_STATUS['pending']:
                table_id = existingTable["_id"]
            table = self.create_table(league_code, teams, timeFrame, table_id)
            return table
        else:
            self.logger.debug(f"Table found in database") 
            return existingTable

    def get_title_table(self, league_code, teams=None, timeFrame=None, rank=None):
        if rank is None:
            rank = 0
        elif rank == 'won':
            rank = 0

        title_table = {}

        if timeFrame is None:
            timeFrame = {
                'type': 'season',
                'season_from': 1900,
                'season_to': get_current_season()
            }

        seasons = self._get_seasons_from_timeframe(timeFrame)
        for season in seasons:
            temp_timeframe = {
                'type': 'season',
                'season_from': season,
                'season_to': season
            }
            table = self.get_table(league_code,teams, temp_timeframe)

            if table is not None and table['status'] == self.TABLE_STATUS['done']:
                temp_rank = rank
                if rank == 'last':
                    temp_rank = len(table['standings']) - 1
                elif type(rank) == int:
                    temp_rank = min(rank, len(table['standings'])) - 1

                table_entry = table['standings'][rank]
                if table_entry['teamName'] in title_table:
                    title_table_entry = title_table[table_entry['teamName']]
                    title_table_entry['numberOfTitles'] = title_table_entry['numberOfTitles'] + 1
                    title_table_entry['seasons'].append(season+1)
                    title_table_entry['seasons'].sort()
                    title_table[table_entry['teamName']] = title_table_entry
                else:
                    title_table_entry = {
                        'teamName': table_entry['teamName'],
                        'numberOfTitles': 1,
                        'seasons': [season+1]
                    }
                    title_table[table_entry['teamName']] = title_table_entry

        title_table = list(title_table.values())

        if title_table is None:
            title_table = []
        else:
            title_table.sort(key=lambda x: x['numberOfTitles'], reverse=True)

        return title_table


    def create_table(self, league_code, teams=None, timeFrame=None, table_id=None):
        self.logger.debug(f"Creating table ...") 
        timeFrame = self._check_timeFrame(timeFrame)
        self.logger.debug(f"Loading fixtures from timeframe {timeFrame}") 
        competition = self.get_competition(league_code)
        if competition is None:
            tie_break_rules = DEFAULT_TIE_BREAK_RULES
        else:
            tie_break_rules = competition['metadata']['tie_break_rules']

        point_rule = self._get_point_rule_from_timeframe(competition, timeFrame)

        fixtures = self.get_fixtures(league_code=league_code, teams=teams, timeFrame=timeFrame)

        self.logger.debug(f"Found {len(fixtures)} fixtures")

        if len(fixtures) == 0:
            return None

        table_status = self.TABLE_STATUS['done']
        next_update = None

        for fixture in fixtures:
            fixture = self.enrich_fixture(fixture)
            if fixture["dateObject"] > datetime.datetime.now() - datetime.timedelta(hours=2):
                table_status = self.TABLE_STATUS['pending']
                if next_update is None:
                    next_update = datetime.datetime.now() + datetime.timedelta(minutes=5)
                    break

        if table_status == self.TABLE_STATUS['pending']:
            self.logger.debug(f"The table needs to be updated at {next_update}")

        self.logger.debug(f"Computing standings with point rule {point_rule} ...") 
        standings = self.compute_team_standings(fixtures, teams, point_rule=point_rule)
        self.logger.debug(f"Sorting ...") 
        standings = self.sort_league_table(standings, fixtures, point_rule=point_rule, tie_break_rules=tie_break_rules) 
        table = {
            "league_code": league_code,
            "teams": teams,
            "timeFrame": timeFrame,
            "standings": standings,
            "status": table_status,
            "next_update": next_update,
            "point_rule": point_rule,
        }

        self.logger.debug(f"Storing in database ...") 
        if table_id is not None:
            self.collections["tables"].update_one({'_id': table_id}, {'$set': table})
        else:
            self.collections["tables"].insert(table)

        self.logger.debug(f"Table created") 
        return table

    def enrich_fixture(self, fixture):
        fixture = super(TMConnector, self).enrich_fixture(fixture)
        if "date" in fixture:
            fixture["dateObject"] = fixture["date"]
        else:
            fixture["dateObject"] = datetime.datetime(datetime.MINYEAR, 1, 1)
        return fixture

    def get_current_matchday(self, league_code):
        fixture = list(self.collections["fixtures"].find({'league_code':league_code,"date": {"$gte": datetime.datetime.now()}}).sort("date", ASCENDING).limit(1))
        if len(fixture) == 0:
            return 1
        else:
            return fixture[0]["matchday"]

    def get_competition(self, league_code):
        return self.collections["competitions"].find_one({'league_code': league_code})

    def get_ranks_of_teams(self, league_code, teams, timeFrame):
        ranks = {}
        team_ids = self._get_team_ids_from_teams(teams)

        if timeFrame is None:
            timeFrame = {
                'type': 'season',
                'season_from': 1900,
                'season_to': get_current_season()
            }

        seasons = self._get_seasons_from_timeframe(timeFrame)

        for season in seasons:
            temp_timeframe = {
                'type': 'season',
                'season_from': season,
                'season_to': season
            }
            table = self.get_table(league_code, None, temp_timeframe)

            if table is not None:
                ranks[season] = {}
                standings = table['standings']

                for standing in standings:
                    if standing['teamId'] in team_ids:
                        ranks[season][standing['teamId']] = standing['position']

        return ranks

    def get_scorer_table(self, league_code=None, teams=None, players=None, timeFrame=None, goals=False, assists=False):
        if league_code is None and players is None and teams is None:
            return None
    
        timeFrame = self._check_timeFrame(timeFrame)
        fixtures = self.get_fixtures(league_code=league_code, teams=teams, players=players, timeFrame=timeFrame)
        score_table = self.compute_scorer_table(fixtures, players=players, goals=goals, assists=assists)
        return score_table

    def search_player(self, query):
        query = query.translate({ ord(c): None for c in string.whitespace }).lower()
        ngrams = make_ngrams(query)
        search_string = " ".join([str(x) for x in ngrams])  
        return list(self.collections['players.search'].find({
                "$text": {
                    "$search": search_string
                }
            }, {
                "player_id": True,
                "name": True,
                "score": {
                    "$meta": "textScore"
                }
            }
        ).sort([("score", {"$meta": "textScore"})]))

    def search_team(self, query):
        query = query.translate({ ord(c): None for c in string.whitespace }).lower()
        ngrams = make_ngrams(query)
        search_string = " ".join([str(x) for x in ngrams])  
        return list(self.collections['teams.search'].find({
                "$text": {
                    "$search": search_string
                }
            }, {
                "team_id": True,
                "crest_url": True,
                "name": True,
                "score": {
                    "$meta": "textScore"
                }
            }
        ).sort([("score", {"$meta": "textScore"})]))
