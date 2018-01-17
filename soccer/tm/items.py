# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=True)
    competitions = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False, isSearchField=False)

class TeamSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    competition = Field(existCheck=True, updateable=False, isArray=False, isDict=True, arrayReplace=False, isSearchField=False)
    players = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False, isSearchField=False)

class CompetitionItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    icon = Field(existCheck=False, updateable=True, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=False, arrayReplace=False, isSearchField=False)
    metadata = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False)

class CompetitionSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    teams = Field(existCheck=False, updateable=False, isArray=True, isDict=True, arrayReplace=True, isSearchField=False)

class PlayerItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    player_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=True)
    birthday = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    country = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False, isSearchField=False)

class FixtureItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    date = Field(existCheck=False, updateable=True, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    matchday = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    homeTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    awayTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    result = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False)
    referee = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False)
    stadium = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False)
    goals = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False)
    assists = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False)
    cards = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False)
    lineups = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False)