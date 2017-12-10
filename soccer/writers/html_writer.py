""" HTML writer """
from soccer.writers import BasicWriter

class HTMLWriter(BasicWriter):
    """
    HTML writer
    """
    def __init__(self):
        pass

    def league_table(self, table):
        html = "<table><thead><tr><th>#</th><th>Team</th><th>P</th><th>W</th><th>D</th><th>L</th><th>Goals</th><th>Pts</th></tr></thead><tbody>"

        for team in table["standings"]:
            html = html + f"<tr><th>{team['position']}</th><th>{team['teamName']}</th><th>{team['playedGames']}</th><th>{team['wins']}</th><th>{team['draws']}</th><th>{team['losses']}</th><th>{team['goals']}:{team['goalsAgainst']}</th><th>{team['points']}</th></tr>"

        html = html + "</tbody></table>"
        return html