""" Bootstrap writer """
import logging
import random
import hashlib
from hashlib import md5
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

        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='datatable table table-striped table-hover table-sm' style='width:100%'><thead><tr><th data-priority='4'>#</th><th data-priority='1'>Team</th><th data-priority='3'>P</th><th>W</th><th>D</th><th>L</th><th data-priority='6'>Goals</th><th data-priority='5'>Diff</th><th data-priority='2'>Pts</th></tr></thead><tbody>"

        try:
            display_negative_points = POINT_RULES[table['point_rule']]['DISPLAY_NEGATIVE_POINTS']
        except KeyError:
            display_negative_points = DEFAULT_POINT_RULE_DISPLAY_NEGATIVE_POINTS

        for team in table["standings"]:
            if display_negative_points is True:
                points = str(team['points']) + ":" + str(team['negative_points'])
            else:
                points = str(team['points'])

            crest_img = self._get_crest_img(team)

            html = html + f"<tr><td>{team['position']}</td><td>{crest_img+team['teamName']}</td><td>{team['playedGames']}</td><td>{team['wins']}</td><td>{team['draws']}</td><td>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td>{team['goals']-team['goalsAgainst']}</td><td>{points}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def rank_table(self, table, rank=None, teams=None):
        if rank is None and teams is None:
            return self.league_table(table)

        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='table table-striped table-hover table-sm' style='width:100%'><thead><tr><th data-priority='4'>#</th><th data-priority='1'>Team</th><th data-priority='3'>P</th><th>W</th><th>D</th><th>L</th><th data-priority='6'>Goals</th><th data-priority='5'>Diff</th><th data-priority='2'>Pts</th></tr></thead><tbody>"

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

            crest_img = self._get_crest_img(team)

            if pos == rank:
                html = html + f"<tr class='table-success'><td>{team['position']}</td><td>{crest_img+team['teamName']}</td><td>{team['playedGames']}</td><td>{team['wins']}</td><td>{team['draws']}</td><td>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td>{team['goals']-team['goalsAgainst']}</td><td>{points}</td></tr>"
            else:
                html = html + f"<tr><td>{team['position']}</td><td>{crest_img+team['teamName']}</td><td>{team['playedGames']}</td><td>{team['wins']}</td><td>{team['draws']}</td><td>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td>{team['goals']-team['goalsAgainst']}</td><td>{points}</td></tr>"

        if rank and rank < len(table["standings"]) - 3:
            html = html + f"<tr><td colspan='9' class='text-center'>...</td></tr>"

        html = html + "</tbody></table>"
        return html

    def title_table(self, title_table):
        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='table table-striped table-hover table-sm' style='width:100%'><thead><tr><th>Team</th><th>#</th><th>Seasons</th></tr></thead><tbody>"
        
        for team in title_table:
            crest_img = self._get_crest_img(team)
            html = html + f"<tr><td>{crest_img+team['teamName']}</td><td>{team['numberOfTitles']}</td><td>{', '.join(str(season) for season in team['seasons'])}</td></tr>"
        
        html = html + "</tbody></table>"
        return html

    def fixture_list(self, fixtures):
        if fixtures is None:
            return "No fixtures found"
        
        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='table table-striped table-hover table-sm datatablePaging' style='width:100%'><thead><tr><th>Date</th></th><th class='text-right' data-priority='1'>Home</th><th colspan='3' class='text-center' data-priority='1'>Result</th><th data-priority='1'>Away</th></tr></thead><tbody>"

        for fixture in fixtures:
            html = html + f"<tr><td>{fixture['date'].strftime('%x %X')}</td><td class='text-right'>{fixture['homeTeam']['name']}</td><td class='text-right'>{fixture['result']['goalsHomeTeam']}</td><td class='text-center'>:</td><td class='text-left'>{fixture['result']['goalsAwayTeam']}</td><td>{fixture['awayTeam']['name']}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def ranks_of_teams(self, ranks_of_teams, teams=None, rank=None):
        if teams is None:
            return ""

        seasons = ranks_of_teams.keys()

        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='datatable table table-striped table-hover table-sm' style='width:100%'><thead><tr><th>Team</th>"

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

    def rank_and_titles(self, rank_table, ranks_of_teams, teams=None, rank=None):
        rank_table_html = self.rank_table(rank_table, rank=rank, teams=teams)
        ranks_of_teams_html = self.ranks_of_teams(ranks_of_teams, teams=teams)

        random_id = random.randint(0, 99999)

        html = "<ul class='nav nav-tabs'><li class='active'><a data-toggle='tab' href='#seasons_" + str(random_id) + "'>Separate Seasons</a></li><li><a data-toggle='tab' href='#combinedtable_" + str(random_id) + "'>Combined Table</a></li></ul>"
        html = html + "<div class='tab-content'><div id='seasons_" + str(random_id) + "' class='tab-pane fade in active'><p>"
        html = html + ranks_of_teams_html
        html = html + "</p></div><div id='combinedtable_" + str(random_id) + "' class='tab-pane fade'><p>"
        html = html + rank_table_html
        html = html + "</p></div></div>"

        return html    
    
    def title_table_and_rank_table(self, title_table, rank_table, rank=None):
        title_table_html = self.title_table(title_table)
        rank_table_html =  self.rank_table(rank_table, rank=rank) 

        random_id = random.randint(0, 99999)

        html = "<ul class='nav nav-tabs'><li class='active'><a data-toggle='tab' href='#seasons_" + str(random_id) + "'>Separate Seasons</a></li><li><a data-toggle='tab' href='#combinedtable_" + str(random_id) + "'>Combined Table</a></li></ul>"
        html = html + "<div class='tab-content'><div id='seasons_" + str(random_id) + "' class='tab-pane fade in active'><p>"
        html = html + title_table_html
        html = html + "</p></div><div id='combinedtable_" + str(random_id) + "' class='tab-pane fade'><p>"
        html = html + rank_table_html
        html = html + "</p></div></div>"

        return html

    def goal_table(self, goal_table, player=None):
        if goal_table is None:
            return ""
        else:
            goal_table.sort(key=lambda x: x['goals'], reverse=True)

        if len(goal_table) > 30:
            datatable_class = "datatablePaging"
        else:
            datatable_class = "datatable"

        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='table table-striped table-hover table-sm " + datatable_class + "' style='width:100%'><thead><tr><th data-priority='1'>Player</th><th>Team</th><th data-priority='3'>P</th><th data-priority='2'>G</th></tr></thead><tbody>"

        for player_goals in goal_table:
            if player is not None and player_goals['player_id'] == player['player_id']:
                html = html + f"<tr class='table-success'><td>{player_goals['player_name']}</td><td>{', '.join(player_goals['team'])}</td><td>{player_goals['playedGames']}</td><td>{player_goals['goals']}</td></tr>"
            else:
                html = html + f"<tr><td>{player_goals['player_name']}</td><td>{', '.join(player_goals['team'])}</td><td>{player_goals['playedGames']}</td><td>{player_goals['goals']}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def multi_table(self, tables, teams=None, rank=None):
        random_id = str(random.randint(0, 99999))
        html = "<ul class='nav nav-tabs'>"

        for idx, (key, data) in enumerate(tables.items()):
            data['id'] = md5(data['name'].encode('utf-8')).hexdigest() + "_" + random_id
            if idx == 0:
                html = html + f"<li class='active'><a data-toggle='tab' href='#{data['id']}'>{data['name']}</a></li>"
            else:
                html = html + f"<li><a data-toggle='tab' href='#{data['id']}'>{data['name']}</a></li>"

        html = html + "</ul><div class='tab-content'>"

        for idx, (key, data) in enumerate(tables.items()):
            table = data['table']

            if idx == 0:
                html = html + f"<div id='{data['id']}' class='tab-pane fade in active'><p>"
            else:
                html = html + f"<div id='{data['id']}' class='tab-pane fade'><p>"

            if key == "league_table":
                table_html = self.league_table(table)
            elif key == "rank_table":
                table_html = self.rank_table(table, teams=teams, rank=rank)
            elif key == "title_table":
                table_html = self.title_table(table)
            elif key == "ranks_of_teams":
                table_html = self.ranks_of_teams(table, teams=teams, rank=rank)
            elif key == "h2h_table":
                table_html = self.league_table(table)
            else:
                table_html = self.league_table(table)
            
            html = html + table_html + "</p></div>"

        html = html + "</div>"
        return html

    def assist_table(self, assist_table, player=None):
        if assist_table is None:
            return ""
        else:
            assist_table.sort(key=lambda x: x['assists'], reverse=True)

        if len(assist_table) > 30:
            datatable_class = "datatablePaging"
        else:
            datatable_class = "datatable"

        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='table table-striped table-hover table-sm " + datatable_class + "' style='width:100%'><thead><tr><th data-priority='1'>Player</th><th>Team</th><th data-priority='3'>P</th><th data-priority='2'>A</th></tr></thead><tbody>"

        for player_assists in assist_table:
            if player is not None and player_assists['player_id'] == player['player_id']:
                html = html + f"<tr class='table-success'><td>{player_assists['player_name']}</td><td>{', '.join(player_assists['team'])}</td><td>{player_assists['playedGames']}</td><td>{player_assists['assists']}</td></tr>"
            else:
                html = html + f"<tr><td>{player_assists['player_name']}</td><td>{', '.join(player_assists['team'])}</td><td>{player_assists['playedGames']}</td><td>{player_assists['assists']}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def scorer_table(self, scorer_table, player=None):
        if scorer_table is None:
            return ""
        else:
            scorer_table.sort(key=lambda x: x['scorers'], reverse=True)

        if len(scorer_table) > 30:
            datatable_class = "datatablePaging"
        else:
            datatable_class = "datatable"

        random_id = random.randint(0, 99999)

        html = "<table id='table_" + str(random_id) + "' class='table table-striped table-hover table-sm " + datatable_class + "' style='width:100%'><thead><tr><th data-priority='1'>Player</th><th>Team</th><th data-priority='4'>P</th><th data-priority='3'>G</th><th data-priority='3'>A</th><th data-priority='2'>S</th></tr></thead><tbody>"

        for player_scorers in scorer_table:
            if player is not None and player_scorers['player_id'] == player['player_id']:
                html = html + f"<tr class='table-success'><td>{player_scorers['player_name']}</td><td>{', '.join(player_scorers['team'])}</td><td>{player_scorers['playedGames']}</td><td>{player_scorers['goals']}</td><td>{player_scorers['assists']}</td><td>{player_scorers['goals'] + player_scorers['assists']}</td></tr>"
            else:
                html = html + f"<tr><td>{player_scorers['player_name']}</td><td>{', '.join(player_scorers['team'])}</td><td>{player_scorers['playedGames']}</td><td>{player_scorers['goals']}</td><td>{player_scorers['assists']}</td><td>{player_scorers['goals'] + player_scorers['assists']}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def _get_crest_img(self, team, height=30):
        if 'crest_url' in team and team['crest_url'] is not None:
            crest_img = f"<img src='{team['crest_url']}' alt='{team['teamName']}' height='{height}' style='padding:3px;'/>"
        else:
            crest_img = ""
        
        return crest_img
