from pymongo import MongoClient
from urllib.parse import quote_plus


uri = "mongodb://%s:%s@%s:%s" % (
    quote_plus("soccer"), quote_plus("***REMOVED***"), "localhost", "27017")

client = MongoClient(uri,authSource="user-data")

db = client["soccer-data"]
collections = {
    "teams": db["teams"],
    "team_season": db["team_season"],
    "competitions": db["competitions"],
    "competition_season": db["competition_season"],
    "players": db["players"],
    "player_season": db["player_season"]
}

print(db["fixtures"].find_one())