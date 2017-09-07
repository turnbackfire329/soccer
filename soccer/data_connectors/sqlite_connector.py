"""
SQLite Connector for soccer data. This connector
expects the european soccer dataset that can be found here:
https://www.kaggle.com/hugomathien/soccer
"""
import sqlite3

from .data_connector import DataConnector

class SQLiteConnector(DataConnector):
    """
    SQLite Connector for soccer data. This connector
    expects the european soccer dataset that can be found here:
    https://www.kaggle.com/hugomathien/soccer
    """
    def __init__(self, db_path):
        DataConnector.__init__(self)
        self.db = sqlite3.connect(db_path)
