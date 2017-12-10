""" Bootstrap writer """
from soccer.writers import BasicWriter

class BootstrapWriter(BasicWriter):
    """
    Bootstrap writer
    """
    def __init__(self):
        pass

    def league_table(self, table):
        html = "<table class='table table-striped table-hover'><thead><tr><th>#</th><th>Team</th><th>P</th><th class='hidden-xs'>W</th><th class='hidden-xs'>D</th><th class='hidden-xs'>L</th><th>Goals</th><th class='hidden-xs'>Diff</th><th>Pts</th></tr></thead><tbody>"

        for team in table["standings"]:
            html = html + f"<tr><td>{team['position']}</td><td>{team['teamName']}</td><td>{team['playedGames']}</td><td class='hidden-xs'>{team['wins']}</td><td class='hidden-xs'>{team['draws']}</td><td class='hidden-xs'>{team['losses']}</td><td>{team['goals']}:{team['goalsAgainst']}</td><td class='hidden-xs'>{team['goals']-team['goalsAgainst']}</td><td>{team['points']}</td></tr>"

        html = html + "</tbody></table>"
        return html