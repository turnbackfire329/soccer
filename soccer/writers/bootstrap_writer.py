""" Bootstrap writer """
import logging
import random
from soccer.writers import BasicWriter
from ..util import POINT_RULES, DEFAULT_POINT_RULE_DISPLAY_NEGATIVE_POINTS, season_to_string

class BootstrapWriter(BasicWriter):
    """
    Bootstrap writer
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def league_table(self, table):
        if table is None:
            return "I could not calculate a table. Maybe the season does not exist or no fixtures have been played?"
        html = "<table class='datatable table table-striped table-hover table-condensed'><thead><tr><th>#</th><th>Team</th><th>P</th><th class='hidden-xs'>W</th><th class='hidden-xs'>D</th><th class='hidden-xs'>L</th><th>Goals</th><th class='hidden-xs'>Diff</th><th>Pts</th></tr></thead><tbody>"

        try:
            display_negative_points = POINT_RULES[table['point_rule']]['DISPLAY_NEGATIVE_POINTS']
        except KeyError:
            display_negative_points = DEFAULT_POINT_RULE_DISPLAY_NEGATIVE_POINTS

        for team in table["standings"]:
            if display_negative_points is True:
                points = str(team['points']) + ":" + str(team['negative_points'])
            else:
                points = str(team['points'])

            html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{points}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def rank_table(self, table, rank=None, teams=None):
        if rank is None and teams is None:
            return self.league_table(table)

        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th>#</th><th>Team</th><th>P</th><th class='hidden-xs'>W</th><th class='hidden-xs'>D</th><th class='hidden-xs'>L</th><th>Goals</th><th class='hidden-xs'>Diff</th><th>Pts</th></tr></thead><tbody>"

        try:
            display_negative_points = POINT_RULES[table['point_rule']]['DISPLAY_NEGATIVE_POINTS']
        except KeyError:
            display_negative_points = DEFAULT_POINT_RULE_DISPLAY_NEGATIVE_POINTS

        start_pos = 0
        end_pos = len(table['standings'])

        if teams is not None:
            if len(teams) == 1:
                team = teams[0]
                for standing in table['standings']:
                    if standing['teamId'] == team['team_id']:
                        rank = standing['position'] - 1 
                        start_pos = rank - 2
                        end_pos = rank + 3
                        break
            else:
                rank = None
        else:
            if rank == "won":
                rank = 0
            elif rank == "last":
                rank = len(table["standings"]) - 1
            elif type(rank) == int:
                rank = min(rank, len(table["standings"])) - 1
            else:
                rank = 0

            start_pos = rank - 2
            end_pos = rank + 3

        if start_pos > 2:
            html = html + f"<tr><td colspan='9' class='text-center'>...</td></tr>"

        for pos in range(max(0, start_pos), min(end_pos, len(table["standings"]))):
            team = table["standings"][pos]

            if display_negative_points is True:
                points = str(team['points']) + ":" + str(team['negative_points'])
            else:
                points = str(team['points'])

            if pos == rank:
                html = html + f"<tr class='success'><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{points}</td></tr>"
            else:
                html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{points}</td></tr>"

        if rank and rank < len(table["standings"]) - 3:
            html = html + f"<tr><td colspan='9' class='text-center'>...</td></tr>"

        html = html + "</tbody></table>"
        return html

    def title_table(self, title_table):
        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th>Team</th><th>#</th><th>Seasons</th></tr></thead><tbody>"
        
        for team in title_table:
            html = html + f"<tr><td>{team['teamName']}</td><td>{team['numberOfTitles']}</td><td>{', '.join(str(season) for season in team['seasons'])}</td></tr>"
        
        html = html + "</tbody></table>"
        return html

    def fixture_list(self, fixtures):
        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th class='hidden-xs'>Date</th></th><th class='text-right'>Home</th><th colspan='3' class='text-center'>Result</th><th>Away</th></tr></thead><tbody>"

        for fixture in fixtures:
            html = html + f"<tr><td class='hidden-xs'>{fixture['date'].strftime('%x %X')}</td><td class='text-right'>{fixture['homeTeam']['name']}</td><td class='text-right'>{fixture['result']['goalsHomeTeam']}</td><td class='text-center'>:</td><td class='text-left'>{fixture['result']['goalsAwayTeam']}</td><td>{fixture['awayTeam']['name']}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def ranks_teams(self, ranks_of_teams, teams=None):
        if teams is None:
            return ""

        seasons = ranks_of_teams.keys()

        html = "<table class='datatable table table-striped table-hover table-condensed'><thead><tr><th>Team</th>"

        for season in seasons:
            html = html + "<th>" + season_to_string(season) + "</th>"

        html = html + "</tr></thead><tbody>"

        for team in teams:
            html = html + f"<tr><td>{team['name']}</td>"
            for season in seasons:
                if team['team_id'] in ranks_of_teams[season]:
                    position = ranks_of_teams[season][team['team_id']]
                else:
                    position = "-"
                html = html + f"<td>{position}</td>"

        html = html + "</tbody></table>"

        return html

    def rank_and_titles(self, rank_table, ranks_of_teams, teams=None):
        rank_table_html = self.rank_table(rank_table, teams=teams)
        ranks_of_teams_html = self.ranks_teams(ranks_of_teams, teams=teams)

        random_id = random.randint(0, 99999)

        html = "<ul class='nav nav-tabs'><li class='active'><a data-toggle='tab' href='#seasons_" + str(random_id) + "'>Separate Seasons</a></li><li><a data-toggle='tab' href='#combinedtable_" + str(random_id) + "'>Combined Table</a></li></ul>"
        html = html + "<div class='tab-content'><div id='seasons_" + str(random_id) + "' class='tab-pane fade in active'><p>"
        html = html + ranks_of_teams_html
        html = html + "</p></div><div id='combinedtable_" + str(random_id) + "' class='tab-pane fade'><p>"
        html = html + rank_table_html
        html = html + "</p></div></div>"

        return html

    def goal_table(self, goal_table, player=None):
        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th>Player</th><th>P</th><th>G</th></tr></thead><tbody>"

        for player_goals in goal_table:
            if player is not None and player_goals['player_id'] == player['player_id']:
                html = html + f"<tr class='success'><td>{player_goals['name']}</td><td>{player_goals['playedGames']}</td><td>{player_goals['goals']}</td></tr>"
            else:
                html = html + f"<tr><td>{player_goals['name']}</td><td>{player_goals['playedGames']}</td><td>{player_goals['goals']}</td></tr>"

        html = html + "</tbody></table>"
        return html
    
    def assist_table(self, assist_table, player=None):
        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th>Player</th><th>P</th><th>A</th></tr></thead><tbody>"

        for player_assists in assist_table:
            if player is not None and player_assists['player_id'] == player['player_id']:
                html = html + f"<tr class='success'><td>{player_assists['name']}</td><td>{player_assists['playedGames']}</td><td>{player_assists['assists']}</td></tr>"
            else:
                html = html + f"<tr><td>{player_assists['name']}</td><td>{player_assists['playedGames']}</td><td>{player_assists['assists']}</td></tr>"

        html = html + "</tbody></table>"
        return html