# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=True, searchWeight=100)
    competitions = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)
    crest_url = Field(existCheck=False, updateable=True, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)

class TeamSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    team_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    competition = Field(existCheck=True, updateable=False, isArray=False, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)
    players = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)

class CompetitionItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    icon = Field(existCheck=False, updateable=True, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    metadata = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)

class CompetitionSeasonItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    teams = Field(existCheck=False, updateable=False, isArray=True, isDict=True, arrayReplace=True, isSearchField=False, searchWeight=0)

class PlayerItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    player_id = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    name = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=True, searchWeight=200)
    firstname = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=True, searchWeight=100)
    lastname = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=True, searchWeight=300)
    birthday = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    country = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    seasons = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)

class FixtureItem(Item):
    _id = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    collection = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    date = Field(existCheck=False, updateable=True, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    matchday = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    homeTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    awayTeam = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    result = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)
    season = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    league_code = Field(existCheck=True, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    url = Field(existCheck=False, updateable=False, isArray=False, isDict=False, arrayReplace=False, isSearchField=False, searchWeight=0)
    referee = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)
    stadium = Field(existCheck=False, updateable=True, isArray=False, isDict=True, arrayReplace=False, isSearchField=False, searchWeight=0)
    goals = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False, searchWeight=0)
    assists = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False, searchWeight=0)
    cards = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False, searchWeight=0)
    lineups = Field(existCheck=False, updateable=True, isArray=True, isDict=True, arrayReplace=True, isSearchField=False, searchWeight=0)
