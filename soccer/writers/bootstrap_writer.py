""" Bootstrap writer """
import logging
from soccer.writers import BasicWriter

class BootstrapWriter(BasicWriter):
    """
    Bootstrap writer
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def league_table(self, table):
        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th>#</th><th>Team</th><th>P</th><th class='hidden-xs'>W</th><th class='hidden-xs'>D</th><th class='hidden-xs'>L</th><th>Goals</th><th class='hidden-xs'>Diff</th><th>Pts</th></tr></thead><tbody>"

        for team in table["standings"]:
            html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{team['points']}</td></tr>"

        html = html + "</tbody></table>"
        return html

    def rank_table(self, table, position):
        html = "<table class='table table-striped table-hover table-condensed'><thead><tr><th>#</th><th>Team</th><th>P</th><th class='hidden-xs'>W</th><th class='hidden-xs'>D</th><th class='hidden-xs'>L</th><th>Goals</th><th class='hidden-xs'>Diff</th><th>Pts</th></tr></thead><tbody>"

        if position == "won":
            position = 0
        elif position == "last":
            position = len(table["standings"]) - 1
        elif type(position) == int:
            position = min(position, len(table["standings"])) - 1
        else:
            position = 0

        if position > 2:
            html = html + f"<tr><td colspan='9' class='text-center'>...</td></tr>"

        for pos in range(max(0,position-2), min(position+3, len(table["standings"]))):
            team = table["standings"][pos]
            if pos == position:
                html = html + f"<tr class='success'><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{team['points']}</td></tr>"
            else:
                html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{team['points']}</td></tr>"

        if position < len(table["standings"]) - 3:
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