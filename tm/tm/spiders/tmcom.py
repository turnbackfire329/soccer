# -*- coding: utf-8 -*-
import scrapy
import re
import string
import logging
import datetime
import string
from tm.items import TeamItem, TeamSeasonItem, CompetitionItem, CompetitionSeasonItem, PlayerItem, FixtureItem
from bson import ObjectId


class TmcomSpider(scrapy.Spider):
    name = 'tmcom'
    allowed_domains = ['transfermarkt.com']
    # start_urls = ['https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1',
    #                'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
    #                'https://www.transfermarkt.com/2-bundesliga/startseite/wettbewerb/L2',
    #                'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1']
    start_urls = ['https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1']

    start_url_dict = {
        '/1-bundesliga/startseite/wettbewerb/L1': 'BL1',
        '/2-bundesliga/startseite/wettbewerb/L2': 'BL2',
        '/3-liga/startseite/wettbewerb/L3': 'BL3',
        '/premier-league/startseite/wettbewerb/GB1': 'PL',
        '/league-one/startseite/wettbewerb/GB3': 'EL1',
        '/championship/startseite/wettbewerb/GB2': 'ELC',
        '/serie-a/startseite/wettbewerb/IT1': 'SA',
        '/serie-b/startseite/wettbewerb/IT2': 'SB',
        '/laliga/startseite/wettbewerb/ES1': 'PD',
        '/laliga2/startseite/wettbewerb/ES2': 'SD',
        '/ligue-1/startseite/wettbewerb/FR1': 'FL1',
        '/ligue-2/startseite/wettbewerb/FR2': 'Fl2',
    }
    base_url = 'https://www.transfermarkt.com'
    logger = logging.getLogger()

    def parse(self, response):
        item_competition = CompetitionItem(
                _id = ObjectId(),
                collection="competitions"
        )

        item_competition['icon'] = response.css('div .headerfoto > img ::attr(src)').extract_first()
        item_competition['url'] = response.url
        try:
            item_competition['league_code'] = self.start_url_dict[response.url[len(self.base_url):]]
        except KeyError:
            item_competition['league_code'] = None
        
        seasons = response.css('select[name=saison_id] > option ::attr(value)').extract()
        item_competition['seasons'] = seasons
        yield item_competition

        for season in seasons:
            season_url = response.url + '/plus/?saison_id=' + season
            item_competition_season = CompetitionSeasonItem(
                _id = ObjectId(),
                league_code = item_competition['league_code'],
                season = season,
                url = season_url,
                collection = 'competition_season',
                teams = []
            )
            yield scrapy.Request(season_url, callback=self.parseSeason, meta={
                'item_competition_season': item_competition_season
            })
            #break

    def parseSeason(self, response):
        item_competition_season = response.meta['item_competition_season']
        
        teams = response.css(".hauptlink.hide-for-small > a.vereinprofil_tooltip")
        for team in teams:
            item_team_season = TeamSeasonItem(
                _id = ObjectId(),
                name = team.css("::text").extract_first(),
                team_id = team.css("::attr(id)").extract_first(),
                competition = {
                    "season": item_competition_season['season'],
                    "league_code": item_competition_season['league_code']
                },
                url = self.base_url + team.css("::attr(href)").extract_first(),
                collection = "team_season"
            )

            team_url = item_team_season['url'][:item_team_season['url'].find("/saison_id")]
            item_team = TeamItem(
                _id = ObjectId(),
                team_id = item_team_season['team_id'],
                name = item_team_season['name'],
                collection = 'teams',
                url = team_url,
                competitions = [item_team_season["competition"]]
            )

            yield item_team

            yield scrapy.Request(item_team_season['url'], callback=self.parseTeamSeason, meta={
                'item_team_season': item_team_season
            })
            

            item_competition_season['teams'].append({
                'team_id': item_team_season['team_id'],
                'name': item_team_season['name']
            })
            #break
        
        all_fixtures_url = self.base_url + response.css(".footer-links > a ::attr(href)").extract_first()

        yield scrapy.Request(all_fixtures_url, callback=self.parseAllFixtures, meta={
                'item_competition_season': item_competition_season
        })

        yield item_competition_season

    def parseTeam(self, response):
        item_team = response.meta['item_team']
        yield item_team

    def parseTeamSeason(self, response):
        item_team_season = response.meta['item_team_season']
        item_team_season['players'] = []

        players = response.css("div[id=yw1] > table.items > tbody > tr")

        for player in players:
            columns = player.css("td")
            item_player_columns = columns.css("td.posrela > table > tr > td ::text").extract()

            birthday = columns.css(".zentriert ::text").extract()[1].split(" (")[0]
            try:
                birthday = datetime.datetime.strptime(birthday, '%b %d, %Y')
            except ValueError:
                pass

            item_player = PlayerItem(
                _id = ObjectId(),
                name = columns.css("span.hide-for-small > a.spielprofil_tooltip ::text").extract_first(),
                birthday = birthday,
                country = columns.css(".flaggenrahmen ::attr(alt)").extract_first(),
                player_id = columns.css("span.hide-for-small > a.spielprofil_tooltip ::attr(id)").extract_first(),
                url = self.base_url + columns.css("span.hide-for-small > a.spielprofil_tooltip ::attr(href)").extract_first(),
                collection = 'players',
                seasons = [{
                    'season': item_team_season['competition']['season'],
                    'team_id': item_team_season['team_id'],
                    'team_name': item_team_season['name'],
                    'position': item_player_columns[len(item_player_columns)-1],
                    'number': columns.css(".rn_nummer ::text").extract_first()
                }]
            )
            yield item_player
            # yield scrapy.Request(item_player['url'], callback=self.parsePlayer, meta={
            #     'item_player': item_player
            # })

            item_team_season['players'].append({
                'player_id': item_player['player_id'],
                'name': item_player['name'],
                'url': item_player['url']
            })
            #break

        yield item_team_season

    def parsePlayer(self, response):
        item_player = response.meta['item_player']
        yield item_player

    def parseAllFixtures(self, response):
        item_competition_season = response.meta['item_competition_season']

        matchdays = response.css(".large-6.columns > .box")

        for matchday in matchdays:
            matchday_no = matchday.css(".table-header ::text").extract_first().split(".")[0]
            fixtures_or_dates = matchday.css("table > tbody > tr")

            for fixture_or_date in fixtures_or_dates:
                columns = fixture_or_date.css("td")
                if len(columns.extract()) < 5:
                    date_info = columns[0].css("::text").extract()
                    if len(date_info)==3:
                        [x,date,time] = columns[0].css("::text").extract()
                        #time = time.translate(None, string.whitespace)
                        #time = time.translate({ ord(c):None for c in string.whitespace })
                        date = datetime.datetime.strptime(date, "%b %d, %Y")
                else:
                    for idx, column in enumerate(columns):
                        if idx == 3: # home team
                            home_team_id = column.css("a.vereinprofil_tooltip ::attr(id)").extract_first()
                            home_team_url = self.base_url + column.css("a.vereinprofil_tooltip ::attr(href)").extract_first()
                            home_team_name = column.css("a.vereinprofil_tooltip > img ::attr(alt)").extract_first()
                        elif idx == 4: # result
                            goals = column.css("a ::text").extract_first().split(":")
                            url = self.base_url + column.css("a ::attr(href)").extract_first()
                        elif idx == 5: # away team
                            away_team_id = column.css("a.vereinprofil_tooltip ::attr(id)").extract_first()
                            away_team_url = self.base_url + column.css("a.vereinprofil_tooltip ::attr(href)").extract_first()
                            away_team_name = column.css("a.vereinprofil_tooltip > img ::attr(alt)").extract_first()

                    item_fixture = FixtureItem(
                        _id = ObjectId(),
                        collection = "fixtures",
                        date = date,
                        matchday = matchday_no,
                        homeTeam = {
                            'team_id': home_team_id,
                            'url': home_team_url,
                            'name': home_team_name
                        },
                        awayTeam = {
                            'team_id': away_team_id,
                            'url': away_team_url,
                            'name': away_team_name
                        },
                        result = {
                            "goalsHomeTeam": goals[0],
                            "goalsAwayTeam": goals[1]
                        },
                        # competition = {
                        #     'season': item_competition_season['season'],
                        #     'league_code': item_competition_season['league_code']
                        # }
                        season = item_competition_season['season'],
                        league_code= item_competition_season['league_code']
                    )
                    yield item_fixture
            #break