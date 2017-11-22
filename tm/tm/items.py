# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    competitions = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False)

class TeamSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    competition = Field(existCheck=True, updateable=False, isArray=False, isDict=True, arrayReplace=False)
    players = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False)

class CompetitionItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    icon = Field(existCheck=False, updateable=True, isArray=False, isDict=False, arrayReplace=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=False, arrayReplace=False)

class CompetitionSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    teams = Field(existCheck=False, updateable=False, isArray=True, isDict=True, arrayReplace=True)

class PlayerItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    player_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    birthday = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    country = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False)

class FixtureItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    date = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    matchday = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    homeTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    awayTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    result = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False)
    referee = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False)
    stadium = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False)
    goals = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True)
    assists = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True)
    cards = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True)
    lineups = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True)