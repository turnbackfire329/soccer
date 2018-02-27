""" Basic connector that offers the soccer data interface """

import datetime
import logging
from copy import deepcopy
from ..exceptions import InvalidTimeFrameException
from ..util import (
    DEFAULT_POINT_RULE,
    DEFAULT_POINT_RULE_WIN_POINTS,
    DEFAULT_POINT_RULE_DRAW_POINTS,
    DEFAULT_POINT_RULE_DISPLAY_NEGATIVE_POINTS,
    DEFAULT_TIE_BREAK_RULES,
    EMPTY_TEAM_STANDINGS,
    POINT_RULES,
    SORT_OPTIONS,
    TIE_BREAK_RULES,
    get_current_season,
)

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

    def get_competition(self, league_code):
        pass
    
    def get_fixtures(self, league_code=None, teams=None, players=None, timeframe=None, count=None, future=None, home=True, away=True):
        pass

    def get_ranks_of_teams(self, league_code, teams, timeframe):
        pass

    def get_team(self, team_id): 
        return {
            "team_id": team_id,
            "name": "Team " + str(team_id),
            "crest_url": "https://commons.wikimedia.org/wiki/File:Borussia_Dortmund_logo.svg"
        }

    def get_team_by_timeframe(self, team_id, timeframe):
        pass

    def get_player(self, player_id):
        return {
            "player_id": player_id,
            "name": "PLayer " + str(player_id),
    }

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

    def sort_league_table(self, standings, fixtures, sortBy=None, ascending=None, point_rule=DEFAULT_POINT_RULE, tie_break_rules=DEFAULT_TIE_BREAK_RULES):
        if len(standings) < 2:
            return standings

        standings = self._break_ties(standings, 0, len(standings), fixtures, point_rule, tie_break_rules)

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

    def compute_team_standings(self, fixtures, teams=None, home=True, away=True, head2headOnly=False, point_rule=DEFAULT_POINT_RULE):
        teamStandings = {}

        points_for_win = POINT_RULES[point_rule]['WIN_POINTS']
        points_for_draw = POINT_RULES[point_rule]['DRAW_POINTS']

        if teams is not None:
            team_ids = self._get_team_ids_from_teams(teams)
            for team in team_ids:
                teamStandings[team] = deepcopy(EMPTY_TEAM_STANDINGS)
                teamData = self.get_team(team)
                teamStandings[team]["teamName"] = teamData["name"]
                teamStandings[team]["teamId"] = team
                teamStandings[team]["crest_url"] = teamData["crest_url"] if "crest_url" in teamData else None
        else:
            team_ids = None

        for fixture in fixtures:
            fixture = self.enrich_fixture(fixture)
            if fixture["dateObject"] <= datetime.datetime.now() and fixture["result"]["goalsHomeTeam"] != "-":
                homeId = fixture["homeTeam"]["team_id"]
                awayId = fixture["awayTeam"]["team_id"]

                if team_ids is None or (home and homeId in team_ids and (not head2headOnly or awayId in team_ids)):
                    if homeId not in teamStandings:
                        teamStandings[homeId] = deepcopy(EMPTY_TEAM_STANDINGS)
                        teamData = self.get_team(homeId)
                        teamStandings[homeId]["teamName"] = teamData["name"]
                        teamStandings[homeId]["teamId"] = homeId
                        teamStandings[homeId]["crest_url"] = teamData["crest_url"] if "crest_url" in teamData else None

                    teamStandings[homeId]["home"]["goals"] =                teamStandings[homeId]["home"]["goals"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[homeId]["home"]["goalsAgainst"] =         teamStandings[homeId]["home"]["goalsAgainst"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[homeId]["home"]["goalDifference"] =      teamStandings[homeId]["home"]["goals"] - teamStandings[homeId]["home"]["goalsAgainst"]
                    teamStandings[homeId]["home"]["wins"] =                 teamStandings[homeId]["home"]["wins"] + int(fixture["result"]["winsHomeTeam"])
                    teamStandings[homeId]["home"]["draws"] =                teamStandings[homeId]["home"]["draws"] + int(fixture["result"]["drawsHomeTeam"])
                    teamStandings[homeId]["home"]["losses"] =               teamStandings[homeId]["home"]["losses"] + int(fixture["result"]["lossesHomeTeam"])
                    teamStandings[homeId]["goals"] =                        teamStandings[homeId]["goals"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[homeId]["goalsAgainst"] =                 teamStandings[homeId]["goalsAgainst"] + int(fixture["result"]["goalsAwayTeam"])
                    if fixture["result"]["winsHomeTeam"] == 1:
                        teamStandings[homeId]["points"] =                   teamStandings[homeId]["points"] + points_for_win
                    elif fixture["result"]["lossesHomeTeam"] == 1:
                        teamStandings[homeId]["negative_points"] =          teamStandings[homeId]["negative_points"] + points_for_win
                    else:
                        teamStandings[homeId]["points"] =                   teamStandings[homeId]["points"] + points_for_draw
                        teamStandings[homeId]["negative_points"] =          teamStandings[homeId]["negative_points"] + points_for_draw
                    teamStandings[homeId]["playedGames"] =                  teamStandings[homeId]["playedGames"] + 1
                    teamStandings[homeId]["wins"] =                         teamStandings[homeId]["wins"] + int(fixture["result"]["winsHomeTeam"])
                    teamStandings[homeId]["draws"] =                        teamStandings[homeId]["draws"] + int(fixture["result"]["drawsHomeTeam"])
                    teamStandings[homeId]["losses"] =                       teamStandings[homeId]["losses"] + int(fixture["result"]["lossesHomeTeam"])
                    teamStandings[homeId]["goalDifference"] =              teamStandings[homeId]["goals"] - teamStandings[homeId]["goalsAgainst"] 

                if team_ids is None or ( away and awayId in team_ids and (not head2headOnly or homeId in team_ids)):
                    if awayId not in teamStandings:
                        teamStandings[awayId] = deepcopy(EMPTY_TEAM_STANDINGS)
                        teamData = self.get_team(awayId)
                        teamStandings[awayId]["teamName"] = teamData["name"]
                        teamStandings[awayId]["teamId"] = awayId
                        teamStandings[awayId]["crest_url"] = teamData["crest_url"] if "crest_url" in teamData else None
                        
                    teamStandings[awayId]["away"]["goals"] =                teamStandings[awayId]["away"]["goals"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[awayId]["away"]["goalsAgainst"] =         teamStandings[awayId]["away"]["goalsAgainst"] + int(fixture["result"]["goalsHomeTeam"])
                    teamStandings[awayId]["away"]["goalDifference"] =      teamStandings[awayId]["away"]["goals"] - teamStandings[awayId]["away"]["goalsAgainst"]
                    teamStandings[awayId]["away"]["wins"] =                 teamStandings[awayId]["away"]["wins"] + int(fixture["result"]["winsAwayTeam"])
                    teamStandings[awayId]["away"]["draws"] =                teamStandings[awayId]["away"]["draws"] + int(fixture["result"]["drawsAwayTeam"])
                    teamStandings[awayId]["away"]["losses"] =               teamStandings[awayId]["away"]["losses"] + int(fixture["result"]["lossesAwayTeam"])
                    teamStandings[awayId]["goals"] =                        teamStandings[awayId]["goals"] + int(fixture["result"]["goalsAwayTeam"])
                    teamStandings[awayId]["goalsAgainst"] =                 teamStandings[awayId]["goalsAgainst"] + int(fixture["result"]["goalsHomeTeam"])
                    if fixture["result"]["winsAwayTeam"] == 1:
                        teamStandings[awayId]["points"] =                   teamStandings[awayId]["points"] + points_for_win
                    elif fixture["result"]["lossesAwayTeam"] == 1:
                        teamStandings[awayId]["negative_points"] =          teamStandings[awayId]["negative_points"] + points_for_win
                    else:
                        teamStandings[awayId]["points"] =                   teamStandings[awayId]["points"] + points_for_draw
                        teamStandings[awayId]["negative_points"] =          teamStandings[awayId]["negative_points"] + points_for_draw
                    teamStandings[awayId]["playedGames"] =                  teamStandings[awayId]["playedGames"] + 1
                    teamStandings[awayId]["wins"] =                         teamStandings[awayId]["wins"] + int(fixture["result"]["winsAwayTeam"])
                    teamStandings[awayId]["draws"] =                        teamStandings[awayId]["draws"] + int(fixture["result"]["drawsAwayTeam"])
                    teamStandings[awayId]["losses"] =                       teamStandings[awayId]["losses"] + int(fixture["result"]["lossesAwayTeam"])
                    teamStandings[awayId]["goalDifference"] =              teamStandings[awayId]["goals"] - teamStandings[awayId]["goalsAgainst"]

        return list(teamStandings.values())

    def compute_scorer_table(self, fixtures, players=None, goals=False, assists=False):
        scorer_table = []
        player_dict = {}
        player_ids = self._get_player_ids_from_players(players)
        self.logger.debug(f"Computing scorer table for {str(len(fixtures))} fixtures. Players: {str(len(player_ids))}. Goals: {str(goals)}. Assists: {str(assists)}")

        for fixture in fixtures:
            home_lineup = []
            away_lineup = []
            home_subs = []
            away_subs = []

            if 'lineup' in fixture['lineups']['home']:
                home_lineup = fixture['lineups']['home']['lineup']
            if 'lineup' in fixture['lineups']['away']:
                away_lineup = fixture['lineups']['away']['lineup']
            if 'subs' in fixture['lineups']['home']:
                home_subs = fixture['lineups']['home']['subs']
            if 'subs' in fixture['lineups']['away']:
                away_subs = fixture['lineups']['away']['subs']

            for (player, team_name) in [(player, fixture['homeTeam']['name']) for player in home_lineup]+[(player, fixture['awayTeam']['name']) for player in away_lineup]:
                if 'player_id' in player and (players is None or player['player_id'] in player_ids):
                    if player['player_id'] is None:
                        self.logger.info(f"Player ID in lineup is None. Fixture is: {fixture['_id']}")
                    else:
                        if player['player_id'] not in player_dict:
                            player_db = self.get_player(player['player_id'])
                            if player_db is None:
                                self.logger.info(f"Player ID {player['player_id']} does not exist in DB. Fixture is: {fixture['_id']}")
                            else:
                                player_dict[player['player_id']] = {
                                    'goals': 0,
                                    'assists': 0,
                                    'scorers': 0,
                                    'playedGames': 1,
                                    'player_id': player['player_id'],
                                    'player_name': player_db['name'],
                                    'last_fixture': fixture['_id'],
                                    'team': [team_name],
                                }
                        else:
                            if player_dict[player['player_id']]['last_fixture'] != fixture['_id']:
                                player_dict[player['player_id']]['playedGames'] += 1
                                player_dict[player['player_id']]['last_fixture'] = fixture['_id']
                                if team_name not in player_dict[player['player_id']]['team']:
                                    player_dict[player['player_id']]['team'] = player_dict[player['player_id']]['team'] + [team_name]

            for (sub, team_name) in [(sub, fixture['homeTeam']['name']) for sub in home_subs]+[(sub, fixture['awayTeam']['name']) for sub in away_subs]:
                if sub['in']['player_id'] is None:
                    self.logger.info(f"Player ID in substitution is None. Possibly injury when no substitue left. Fixture is: {fixture['_id']}")
                else:
                    if sub['in']['player_id'] not in player_dict:
                            player_db = self.get_player(sub['in']['player_id'])
                            if player_db is None:
                                self.logger.info(f"Player ID {sub['in']['player_id']} does not exist in DB. Fixture is: {fixture['_id']}")
                            else:
                                player_dict[sub['in']['player_id']] = {
                                    'goals': 0,
                                    'assists': 0,
                                    'scorers': 0,
                                    'playedGames': 1,
                                    'player_id': sub['in']['player_id'],
                                    'player_name': player_db['name'],
                                    'last_fixture': fixture['_id'],
                                    'team': [team_name],
                                }
                    else:
                        if player_dict[sub['in']['player_id']]['last_fixture'] != fixture['_id']:
                            player_dict[sub['in']['player_id']]['playedGames'] += 1
                            player_dict[sub['in']['player_id']]['last_fixture'] = fixture['_id']
                            if team_name not in player_dict[sub['in']['player_id']]['team']:
                                player_dict[sub['in']['player_id']]['team'] = player_dict[sub['in']['player_id']]['team'] + [team_name]

            if goals:
                for goal in fixture['goals']:
                    if goal['type'] != 'Own-goal':
                        team_name = fixture['homeTeam']['name'] if goal['team_id'] == fixture['homeTeam']['team_id'] else fixture['awayTeam']['name']
                        if 'player_id' in goal and (players is None or goal['player_id'] in player_ids):
                            if goal['player_id'] not in player_dict:
                                player_db = self.get_player(goal['player_id'])
                                if player_db is None:
                                    self.logger.info(f"Player ID {goal['player_id']} does not exist in DB. Fixture is: {fixture['_id']}")
                                else:
                                    player_dict[goal['player_id']] = {
                                        'goals': 1,
                                        'assists': 0,
                                        'scorers': 1,
                                        'playedGames': 1,
                                        'player_id': goal['player_id'],
                                        'player_name': player_db['name'],
                                        'last_fixture': fixture['_id'],
                                        'team': [team_name],
                                    }
                            else:
                                player_dict[goal['player_id']]['goals'] += 1
                                player_dict[goal['player_id']]['scorers'] += 1
                                if team_name not in player_dict[goal['player_id']]['team']:
                                    player_dict[goal['player_id']]['team'] = player_dict[goal['player_id']]['team'] + [team_name]
            if assists:
                for assist in fixture['assists']:
                    team_name = fixture['homeTeam']['name'] if assist['team_id'] == fixture['homeTeam']['team_id'] else fixture['awayTeam']['name']
                    if 'player_id' in assist and (players is None or assist['player_id'] in player_ids):
                        if assist['player_id'] not in player_dict:
                            player_db = self.get_player(assist['player_id'])
                            if player_db is None:
                                self.logger.info(f"Player ID {assist['player_id']} does not exist in DB. Fixture is: {fixture['_id']}")
                            else:
                                player_dict[assist['player_id']] = {
                                    'goals': 0,
                                    'assists': 1,
                                    'scorers': 1,
                                    'playedGames': 1,
                                    'player_id': assist['player_id'],
                                    'player_name': player_db['name'],
                                    'last_fixture': fixture['_id'],
                                    'team': [team_name],
                                }
                        else:
                            player_dict[assist['player_id']]['assists'] += 1
                            player_dict[assist['player_id']]['scorers'] += 1
                            if team_name not in player_dict[assist['player_id']]['team']:
                                player_dict[assist['player_id']]['team'] = player_dict[assist['player_id']]['team'] + [team_name]

        scorer_table = [x for x in list(player_dict.values()) if (goals == False and assists == False) or (goals == True and x['goals'] > 0) or (assists == True and x['assists'] > 0)]

        return scorer_table

    def _get_seasons_from_timeframe(self, timeframe):
        timeframe = self._check_timeframe(timeframe)

        if timeframe["type"] == 'season' or timeframe["type"] == 'matchday':
            return range(timeframe['season_from'], timeframe['season_to'] + 1)
        else:
            return range(timeframe['date_from'].year - 1, timeframe['date_to'].year - 1)


    def _get_point_rule_from_timeframe(self, competition, timeframe):
        seasons = self._get_seasons_from_timeframe(timeframe)
        point_rule = None
        
        if competition is None:
            self.logger.warning(f"Competition could not be found. Using default point rule.")
            return DEFAULT_POINT_RULE

        if 'metadata' in competition and 'point_rules' in competition['metadata']:
            point_rules = competition['metadata']['point_rules']
            for season in seasons:
                temp_point_rule = self._get_point_rule_for_season(point_rules, season)

                if point_rule is None:
                    point_rule = temp_point_rule
                elif point_rule != temp_point_rule:
                    return DEFAULT_POINT_RULE
        else:
            self.logger.debug(f"Missing point_rule metadata from competition: {competition}")

        if point_rule is None:
            self.logger.warning(f"Using default point rule.")
            return DEFAULT_POINT_RULE

        return point_rule

    def _get_point_rule_for_season(self, point_rules, season):
        for point_rule in point_rules:
            if 'season_from' in point_rule:
                if 'season_to' in point_rule:
                    if season >= point_rule['season_from'] and season <= point_rule['season_to']:
                        return point_rule['rule']
                elif season >= point_rule['season_from']:
                    return point_rule['rule']
            elif 'season_to' in point_rule and season <= point_rule['season_to']:
                return point_rule['rule']
   
        return DEFAULT_POINT_RULE

    def _check_timeframe(self, timeframe=None):
        bValid = False

        if timeframe is None:
            current_season = str(get_current_season())
            timeframe = {
                "type": "season",
                "season_from": current_season,
                "season_to": current_season
            }
            bValid = True
        elif "type" in timeframe:
            timeframeType = timeframe["type"]

            if timeframeType in self.TIME_FRAME_TYPES:
                if timeframeType == "date":
                    if "date_from" in timeframe and "date_to" in timeframe:
                        bValid = True
                elif timeframeType == "season":
                    if "season_from" in timeframe and "season_to" in timeframe:
                        bValid = True
                elif timeframeType == "matchday":
                    if "season_from" in timeframe and "season_to" in timeframe and "matchday_from" in timeframe and "matchday_to" in timeframe:
                        bValid = True
        
        if bValid == False:
            raise InvalidTimeFrameException(f"Invalid time frame given: {timeframe}", timeframe)
        else:
            return timeframe

    def _break_ties(self, standings, start_index, end_index, fixtures, point_rule, tie_break_rules, tie_break_rule_index=0):
        upcoming_h2h = False
        sortBy = ()
        ascending = ()
        for tbr_index in range(tie_break_rule_index, len(tie_break_rules)):
            if TIE_BREAK_RULES[tie_break_rules[tbr_index]]['head2head'] is True:
                upcoming_h2h = True
                break
            else:
                sortBy = sortBy + (TIE_BREAK_RULES[tie_break_rules[tbr_index]]['field'],)

                if TIE_BREAK_RULES[tie_break_rules[tbr_index]]['descending'] is True:
                    ascending = ascending + (-1,)
                else:
                    ascending = ascending + (1,)

        if upcoming_h2h is False:
            sort_standings = standings[start_index:end_index]
            sort_standings.sort(key=lambda x: self._get_sort_tuple(x, sortBy, ascending))
            standings[start_index:end_index] = sort_standings
            return standings[start_index:end_index]
  
        tie_break_rule = TIE_BREAK_RULES[tie_break_rules[tie_break_rule_index]]     

        sortBy = (tie_break_rule['field'],)

        if tie_break_rule['descending'] is True:
            ascending = (-1,)
        else:
            ascending = (1,)

        if tie_break_rule['head2head'] is True:
            teams = []
            for standing in standings[start_index:end_index]:
                teams.append(standing['teamId'])
            h2h_fixtures = self._find_h2h_fixtures(fixtures, teams)
            if len(h2h_fixtures) != len(teams) * (len(teams) - 1):
                if len(tie_break_rules) > tie_break_rule_index+1:
                    return self._break_ties(standings, start_index, end_index, fixtures, point_rule, tie_break_rules,tie_break_rule_index+1)
                else:
                    return standings[start_index:end_index]

            h2h_standings = self.compute_team_standings(h2h_fixtures, point_rule=point_rule)
            h2h_standings.sort(key=lambda x: self._get_sort_tuple(x, sortBy, ascending))
            compare_value = self._deep_get(h2h_standings[0],tie_break_rule['field'])
            compare_index = 0
            compare_standings = [h2h_standings[0]]
            original_standings = deepcopy(h2h_standings)

            standings_with_h2h_sorting = []
            for standing in h2h_standings:
                search_standing = [val for key,val in enumerate(standings) if val['teamId']==standing['teamId']][0]
                standings_with_h2h_sorting.append(search_standing)

            standings[start_index:end_index] = deepcopy(standings_with_h2h_sorting)
        else:
            sort_standings = standings[start_index:end_index]
            sort_standings.sort(key=lambda x: self._get_sort_tuple(x, sortBy, ascending))
            standings[start_index:end_index] = sort_standings
            compare_value = self._deep_get(standings[start_index],tie_break_rule['field'])
            compare_index = 0
            compare_standings = [standings[start_index]]
            original_standings = deepcopy(standings[start_index:end_index])

        for position in range(1, len(original_standings)):
            standing = original_standings[position]

            if self._deep_get(standing,tie_break_rule['field']) == compare_value:
                compare_standings.append(standing)
            else:
                if compare_index < position - 1 and len(tie_break_rules) > tie_break_rule_index+1:
                    standings[start_index + compare_index:start_index + position] = self._break_ties(standings, start_index + compare_index, start_index + position, fixtures, point_rule, tie_break_rules,tie_break_rule_index+1)
                    
                compare_standings = [standing]
                compare_value = self._deep_get(standing,tie_break_rule['field'])
                compare_index = position

        if compare_index < len(original_standings) - 1 and len(tie_break_rules) > tie_break_rule_index+1:
            standings[start_index + compare_index:start_index + len(original_standings)] = self._break_ties(standings, start_index + compare_index, start_index + len(original_standings), fixtures, point_rule, tie_break_rules,tie_break_rule_index+1)
            
        # if tie_break_rule['head2head'] is True:
        #     standings_with_h2h_sorting = []
        #     for standing in original_standings:
        #         search_standing = [val for key,val in enumerate(standings) if val['teamId']==standing['teamId']][0]
        #         standings_with_h2h_sorting.append(search_standing)

        #     standings[start_index:end_index] = deepcopy(standings_with_h2h_sorting)
        # else:
        #     standings[start_index:end_index] = deepcopy(original_standings)

        return standings[start_index:end_index]

    def _find_h2h_fixtures(self, fixtures, teams):
        h2h_fixtures = []

        for fixture in fixtures:
            if fixture['homeTeam']['team_id'] in teams and fixture['awayTeam']['team_id'] in teams and fixture["dateObject"] < datetime.datetime.now() and fixture["result"]["goalsHomeTeam"] != "-":
                h2h_fixtures.append(fixture)
        
        return h2h_fixtures


    def _get_sort_tuple(self, x, sortBy, ascending):
        t = ()
        for i in range(0, len(sortBy)):
            y = deepcopy(x)
            for sb in sortBy[i]:
                y = y[sb]
            t = t + (ascending[i] * y,)
        return t

    def _deep_get(self, d, keys):
        for key in keys:
            if key in d:
                d = d[key]
            else:
                return None
        return d

    def _get_team_ids_from_teams(self, teams):
        if teams is None or not isinstance(teams, list):
            return []
        return [team['team_id'] for team in teams]

    def _get_player_ids_from_players(self, players):
        if players is None or not isinstance(players, list):
            return []
        return [player['player_id'] for player in players]
