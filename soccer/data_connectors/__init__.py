""" Data connectors for the soccer data pi """

from .fdo_connector import FDOConnector
from .tm_connector import TMConnector

__all__ = ['FDOConnector',
           'TMConnector']