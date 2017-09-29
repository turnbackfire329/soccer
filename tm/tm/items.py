# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    competitions = Field(existCheck=False, updateable=True, isArray=True, isDict=True)

class TeamSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    competition = Field(existCheck=False, updateable=False, isArray=False, isDict=True)
    players = Field(existCheck=False, updateable=True, isArray=True, isDict=True)

class CompetitionItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    icon = Field(existCheck=False, updateable=True, isArray=False, isDict=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=False)

class CompetitionSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    teams = Field(existCheck=False, updateable=False, isArray=True, isDict=True)

class PlayerItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    player_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    birthday = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    country = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=True)

class FixtureItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    date = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    matchday = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    homeTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    awayTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    result = Field(existCheck=False, updateable=False, isArray=False, isDict=False)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False)