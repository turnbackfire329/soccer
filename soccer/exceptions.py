""" This module contains the exceptions for the soccer module """

class NoDataConnectorException(Exception):
    '''Raise when there is no data connector for the given season'''
    def __init__(self, message, season, *args):
        self.message = message
        super(NoDataConnectorException, self).__init__(message, season, *args)

class SoccerDBNotFoundException(Exception):
    '''Raise when the soccer database could not be found '''
    def __init__(self, message, *args):
        self.message = message
        super(SoccerDBNotFoundException, self).__init__(message, *args)

class InvalidTimeFrameException(Exception):
    '''Raise when an invalid timeframe object was passed '''
    def __init__(self, message, timeframe, *args):
        self.message = message
        super(InvalidTimeFrameException, self).__init__(message, timeframe, *args)
