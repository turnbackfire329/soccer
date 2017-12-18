# -*- coding: utf-8 -*-
import scrapy
import re
import string
import logging
import datetime
import string
from pymongo import MongoClient
from scrapy.conf import settings
from urllib.parse import quote_plus
from ..items import TeamItem, TeamSeasonItem, CompetitionItem, CompetitionSeasonItem, PlayerItem, FixtureItem
from bson.objectid import ObjectId
from scrapy.http import HtmlResponse


class TmcomSpider(scrapy.Spider):
    name = 'tmcom'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L1',
                  'https://www.transfermarkt.com/2-bundesliga/startseite/wettbewerb/L2',
                  'https://www.transfermarkt.com/3-liga/startseite/wettbewerb/L3',
                  'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1',
                  'https://www.transfermarkt.com/championship/startseite/wettbewerb/GB2',
                  'https://www.transfermarkt.com/league-one/startseite/wettbewerb/GB3',
                  'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT1',
                  'https://www.transfermarkt.com/serie-b/startseite/wettbewerb/IT2',
                  'https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1',
                  'https://www.transfermarkt.com/laliga2/startseite/wettbewerb/ES2',
                  'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR1',
                  'https://www.transfermarkt.com/ligue-2/startseite/wettbewerb/FR2',
                 ]

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
        '/ligue-2/startseite/wettbewerb/FR2': 'FL2',
    }
    base_url = 'https://www.transfermarkt.com'
    logger = logging.getLogger()

    def parse(self, response):
        self.logger.debug(f"Crawl settings: {self.settings.attributes.keys()}")
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

        if self.settings.get("UPDATE_FIXTURES") is not None and self.settings.get("UPDATE_FIXTURES") == 'TRUE':
            self.logger.info("Updating existing fixtures. Loading updateable fixtures from the database ...")
            uri = "mongodb://%s:%s@%s:%s" % (
                quote_plus(settings['MONGODB_USER']), quote_plus(settings['MONGODB_PASSWORD']), settings['MONGODB_SERVER'], settings['MONGODB_PORT'])

            client = MongoClient(uri, authSource=settings['MONGODB_AUTH_DB'])
            db = client[settings['MONGODB_DB']]
            update_fixtures = list(db["fixtures"].find(
                {
                    'league_code': item_competition['league_code'],
                    '$and': [
                        {'date': { '$lte': datetime.datetime.now()}},
                        {'date': { '$gte': datetime.datetime.now() - datetime.timedelta(days=2)}},
                    ],
                }
            ))

            self.logger.info(f"Number of updateable fixtures: {len(update_fixtures)}")
            for fixture in update_fixtures:
                yield scrapy.Request(fixture['url'], callback=self.parseFixture, meta={
                    'item_fixture': FixtureItem(fixture)
                })
        else:
            seasons = [self.settings.get("SEASON")] if self.settings.get("SEASON") is not None else seasons

            if len(seasons) == 1:
                self.logger.info(f"Scraping season {seasons[0]}")
            else:
                self.logger.info(f"Scraping {len(seasons)} seasons")

            for season in seasons:
                season_url = response.url + '/plus/?saison_id=' + season
                item_competition_season = CompetitionSeasonItem(
                    _id=ObjectId(),
                    league_code=item_competition['league_code'],
                    season=int(season),
                    url=season_url,
                    collection='competition_season',
                    teams=[]
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
                _id=ObjectId(),
                name=team.css("::text").extract_first(),
                team_id=team.css("::attr(id)").extract_first(),
                competition={
                    "season": item_competition_season['season'],
                    "league_code": item_competition_season['league_code']
                },
                url=self.base_url + team.css("::attr(href)").extract_first(),
                collection="team_season"
            )

            team_url = item_team_season['url'][:item_team_season['url'].find("/saison_id")]
            item_team = TeamItem(
                _id=ObjectId(),
                team_id=item_team_season['team_id'],
                name=item_team_season['name'],
                collection='teams',
                url=team_url,
                competitions=[item_team_season["competition"]]
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
        all_fixtures = response.css(".footer-links > a ::attr(href)").extract_first()
        if all_fixtures is None:
            self.logger.warning(f"No fixtures for this season: {item_team_season['url']}")
        else:
            all_fixtures_url = self.base_url + all_fixtures
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
                _id=ObjectId(),
                name=columns.css("span.hide-for-small > a.spielprofil_tooltip ::text").extract_first(),
                birthday=birthday,
                country=columns.css(".flaggenrahmen ::attr(alt)").extract_first(),
                player_id=columns.css("span.hide-for-small > a.spielprofil_tooltip ::attr(id)").extract_first(),
                url=self.base_url + columns.css("span.hide-for-small > a.spielprofil_tooltip ::attr(href)").extract_first(),
                collection='players',
                seasons=[{
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
                if len(columns.extract()) > 5:
                    for idx, column in enumerate(columns):
                        if idx == 3: # home team
                            home_team_id = column.css("a.vereinprofil_tooltip ::attr(id)").extract_first()
                            home_team_url = self.base_url + column.css("a.vereinprofil_tooltip ::attr(href)").extract_first()
                            home_team_name = column.css("a.vereinprofil_tooltip > img ::attr(alt)").extract_first()
                        elif idx == 4: # result
                            goals = column.css("a ::text").extract_first().split(":")
                            if len(goals) < 2:
                                goals = ["-","-"]
                            url = self.base_url + column.css("a ::attr(href)").extract_first()
                        elif idx == 5: # away team
                            away_team_id = column.css("a.vereinprofil_tooltip ::attr(id)").extract_first()
                            away_team_url = self.base_url + column.css("a.vereinprofil_tooltip ::attr(href)").extract_first()
                            away_team_name = column.css("a.vereinprofil_tooltip > img ::attr(alt)").extract_first()
                    try:
                        item_fixture = FixtureItem(
                            _id=ObjectId(),
                            collection="fixtures",
                            url=url,
                            matchday=int(matchday_no),
                            homeTeam={
                                'team_id': home_team_id,
                                'url': home_team_url,
                                'name': home_team_name
                            },
                            awayTeam={
                                'team_id': away_team_id,
                                'url': away_team_url,
                                'name': away_team_name
                            },
                            result={
                                "goalsHomeTeam": goals[0],
                                "goalsAwayTeam": goals[1]
                            },
                            season=item_competition_season['season'],
                            league_code=item_competition_season['league_code'],
                            stadium={},
                            referee={},
                            goals=[],
                            assists=[],
                            cards=[]
                        )

                        yield scrapy.Request(url, callback=self.parseFixture, meta={
                            'item_fixture': item_fixture
                        })
                    except (IndexError, ValueError):
                        pass
            #break

    def parseFixture(self, response):
        item_fixture = response.meta['item_fixture']

        # date and time
        try:
            date_information = response.css(".sb-datum.hide-for-small ::text").extract()
            if len(date_information) > 3:
                time = date_information[3].translate({ord(c):None for c in string.whitespace})
                time = time.replace("|","")
                time = time.replace("\xa0", "")
                date = datetime.datetime.strptime(date_information[2] + " " + time, "%a, %b %d, %Y %I:%M%p")
            else:
                date = date_information[2]
                date = datetime.datetime.strptime(date, "%a, %b %d, %Y")

            item_fixture['date'] = date
        except (IndexError, ValueError):
            item_fixture['date'] = datetime.datetime(item_fixture['season'], 12, 31)

        # fulltime score
        try: 
            fulltime = response.css(".sb-endstand ::text").extract()[0].translate({ord(c):None for c in string.whitespace})
            goalsHomeTeam = fulltime.split(":")[0]
            goalsAwayTeam = fulltime.split(":")[1]
            item_fixture['result']['goalsHomeTeam'] = goalsHomeTeam
            item_fixture['result']['goalsAwayTeam'] = goalsAwayTeam
        except IndexError:
            pass

        # halftime score
        try:
            halftime = response.css(".sb-halbzeit ::text").extract()
            goalsHomeTeamHalftime = halftime[1].split(":")[0]
            goalsAwayTeamHalftime = halftime[2].split(")")[0]
            item_fixture['result']['goalsHomeTeamHalftime'] = goalsHomeTeamHalftime
            item_fixture['result']['goalsAwayTeamHalftime'] = goalsAwayTeamHalftime
        except IndexError:
            pass

        #stadium
        stadium_name = response.css(".sb-zusatzinfos > span > a ::text").extract_first()
        item_fixture['stadium']['name'] = stadium_name
        try:
            stadium_url = response.css(".sb-zusatzinfos > span > a ::attr(href)").extract_first()
            item_fixture['stadium']['url'] = self.base_url + stadium_url
        except:
            # no stadium url found
            pass

        # referee
        referee_name = response.css(".sb-zusatzinfos > a ::text").extract_first()
        if referee_name == "open":
            referee_name = "unknown"

        referee_url = response.css(".sb-zusatzinfos > a ::attr(href)").extract_first()
        item_fixture['referee']['name'] = referee_name
        try:
            referee_id = referee_url.split("/")[4]
            item_fixture['referee']['id'] = referee_id
            item_fixture['referee']['url'] = self.base_url + referee_url
        except (IndexError, TypeError, AttributeError):
            pass

        # goals
        goals = response.css("[id=sb-tore] > ul > li")
        item_fixture['goals'], item_fixture['assists'] = self.parseGoals(goals)

        # cards
        cards = response.css("[id=sb-karten] > ul > li")
        item_fixture['cards'] = self.parseCards(cards)

        # lineup
        lineups = response.css(".large-6.columns:not(#schnellsuche-platz)")
        if len(lineups) == 2:
            item_fixture['lineups'] = {
                'home' : self.parseLineup(lineups[0]),
                'away': self.parseLineup(lineups[1])
            }
            if len(item_fixture['lineups']['home']['lineup']) != 11 or len(item_fixture['lineups']['away']['lineup']) != 11:
                self.logger.warning(f"Lineup incomplete: {item_fixture['url']}")
        else:
            self.logger.warning(f"No lineups: {item_fixture['url']}")
            item_fixture['lineups'] = {}

        yield item_fixture

    def parseGoals(self, goalResponse):
        goals = []
        assists = []
        minutes = goalResponse.css(".sb-sprite-uhr-klein ::attr(style)").extract()
        for index, minute in enumerate(minutes):
            [_,column,row] = minute.split(" ")
            column = int(column[1:-2])
            row = int(row[1:-3])
            minutes[index] = int((row / 36 * 10) + (column / 36) + 1)

        scores = goalResponse.css(".sb-aktion-spielstand ::text").extract()
        team_ids = goalResponse.css(".sb-aktion-wappen > .vereinprofil_tooltip ::attr(id)").extract()

        goals_and_assists = goalResponse.css(".sb-aktion-aktion").extract()

        for index, action in enumerate(goals_and_assists):
            action_response = scrapy.http.HtmlResponse(body=action, url="localhost", encoding='utf-8')
            player_names = action_response.css("a ::text").extract()
            player_ids = action_response.css("a ::attr(id)").extract()
            player_urls = action_response.css("a ::attr(href)").extract()
            goal_and_assist = action_response.css("::text").extract()

            for index_goal, goal_or_assist in enumerate(goal_and_assist):
                if index_goal == 2:
                    newGoal = {}
                    newGoal['minute'] = minutes[index]
                    newGoal['goalsHomeTeam'] = scores[index].split(":")[0]
                    newGoal['goalsAwayTeam'] = scores[index].split(":")[1]
                    newGoal['player_name'] = player_names[0]
                    newGoal['player_id'] = player_ids[0]
                    newGoal['player_url'] = self.base_url + player_urls[0]
                    newGoal['type'] = goal_or_assist.split(", ")[1]
                    if "goal" in newGoal['type'] and "season" in newGoal['type']:
                        newGoal['type'] = 'unknown'
                    newGoal['team_id'] = team_ids[index]
                    goals.append(newGoal)

                if index_goal == 5:
                    newAssist = {}
                    newAssist['minute'] = minutes[index]
                    newAssist['goalsHomeTeam'] = scores[index].split(":")[0]
                    newAssist['goalsAwayTeam'] = scores[index].split(":")[1]
                    newAssist['player_name'] = player_names[1]
                    newAssist['player_id'] = player_ids[1]
                    newAssist['player_url'] = self.base_url + player_urls[1]
                    newAssist['team_id'] = team_ids[index]
                    try:
                        newAssist['type'] = goal_or_assist.split(", ")[1]
                        if "assist" in newAssist['type'] and "season" in newAssist['type']:
                            newAssist['type'] = 'unknown'
                        assists.append(newAssist)
                    except IndexError:
                        # player from another team made assist (eg handball that lead to penalty)
                        pass
        return goals, assists

    def parseCards(self, cardResponse):
        cards = []

        minutes = cardResponse.css(".sb-sprite-uhr-klein ::attr(style)").extract()
        for index, minute in enumerate(minutes):
            [_,column,row] = minute.split(" ")
            column = int(column[1:-2])
            row = int(row[1:-3])
            minutes[index] = int((row / 36 * 10) + (column / 36) + 1)

        type_of_cards = cardResponse.css(".sb-aktion-spielstand").extract()
        team_ids = cardResponse.css(".sb-aktion-wappen > .vereinprofil_tooltip ::attr(id)").extract()

        card_infos = cardResponse.css(".sb-aktion-aktion").extract()

        for index, action in enumerate(card_infos):
            newCard = {}
            newCard['minute'] = minutes[index]
            newCard['team_id'] = team_ids[index]
            action_response = scrapy.http.HtmlResponse(body=action, url="localhost", encoding='utf-8')
            newCard['player_name'] = action_response.css("a ::text").extract_first()
            newCard['player_id'] = action_response.css("a ::attr(id)").extract_first()
            newCard['player_url'] = action_response.css("a ::attr(href)").extract_first()
            card_details = action_response.css("::text").extract()[1].split(", ")

            if 'sb-gelb' in type_of_cards[index]:
                newCard['type'] = 'Yellow'
            elif 'sb-rot' in type_of_cards[index]:
                newCard['type'] = 'Red'
            else:
                newCard['type'] = 'Second Yellow'

            if len(card_details) == 1:
                newCard['offense'] = 'unknown'
            else:
                newCard['offense'] = card_details[1]

            cards.append(newCard)
        return cards

    def parseLineup(self, lineup):
        lineup_with_system = lineup.css(".large-7.aufstellung-vereinsseite")
        if len(lineup_with_system) == 2:
            bench = lineup.css(".large-5.aufstellung-ersatzbank-box")[0]
            return {
                'system': self.parseLineupSystem(lineup_with_system[0]),
                'lineup': self.parseLineupPlayers(lineup_with_system[1]),
                'manager': self.parseLineupManager(bench)
            }
        else:
            system = self.parseLineupSystem(lineup.css(".large-12.columns.unterueberschrift.aufstellung-unterueberschrift"))
            playerTable = lineup.css("table > tr > td > a")
            playerArray = []
            manager = {
                'name': 'unknown'
            }

            for player in playerTable:
                url = player.css("::attr(href)").extract_first()
                playerDict = {
                    'url': self.base_url + url,
                    'name': player.css("::text").extract_first(),
                    'id': url.split("/")[4]
                }
                if '/profil/trainer/' in url:
                    manager = playerDict
                else:
                    playerArray.append(playerDict)

            return {
                'system': system,
                'lineup': playerArray,
                'manager': manager
            }


    def parseLineupSystem(self, system):
        sys = system.css("::text").extract_first()
        if sys is None:
            return "unknown"

        return system.css("::text").extract_first().lstrip().rstrip().split(" ")[2]

    def parseLineupPlayers(self, lineup):
        players = lineup.css(".aufstellung-spieler-container > div > span > a")
        playerArray = []

        for player in players:
            url = player.css("::attr(href)").extract_first()
            playerDict = {
                'url': self.base_url + url,
                'name': player.css("::text").extract_first()
            }
            playerDict['playerId'] = url.split("/")[4]
            playerArray.append(playerDict)
        return playerArray

    def parseLineupManager(self, bench):
        manager = bench.css(".ersatzbank > tr > td > a:not(.spielprofil_tooltip)")
        url = manager.css("::attr(href)").extract_first()

        if url is None:
            return {
                'name': manager.css("::text").extract_first()
            }
        else:
            return {
                'url': self.base_url + url,
                'name': manager.css("::text").extract_first(),
                'id': url.split("/")[4]
            }