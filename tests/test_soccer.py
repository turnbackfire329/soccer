# Sample Test passing with nose and pytest

from .context import soccer

soc = soccer.Soccer(db_path='soccerdb/database.sqlite')

def test_season():
    assert "2017" == soc.get_current_season()
    