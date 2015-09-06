import logging

import pandas

from utils.Logger import Logger


class Market(object):
    """
    A Market is a data set (pandas.DataFrame) of Ticker Codes.
    """

    def __init__(self, relativeFilePath):
        """
        Read the Ticker Codes in the specified file into a data set (pandas.DataFrame).

        :param relativeFilePath: Relative file path (String) for the (file) list of ticker codes.
        """

        Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({relativeFilePath})})

        self._relativeFilePath = relativeFilePath

        self.tickers = pandas.read_csv(relativeFilePath)