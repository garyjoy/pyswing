import logging
import datetime
import sqlite3

from utils.Logger import Logger
import pyswing.constants


class Rule(object):
    """
    Rule Base Class.
    """

    def __init__(self, ruleTableName):
        """
        Base Class Constructor.

        :param ?
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        self._ruleTableName = ruleTableName


    def evaluateRule(self, tickerCode):
        """
        ?
        """

        raise NotImplementedError("")


    def _getLatestDate(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = "select max(Date) from '%s' where Code = '%s'" % (self._ruleTableName, self._tickerCode)

        cursor = connection.cursor()

        dateString = None
        try:
            cursor.execute(query)
            dateString = cursor.fetchone()[0]
        except sqlite3.OperationalError:
            Logger.log(logging.INFO, "Table Does Not Exist", {"scope":__name__, "table":self._ruleTableName})

        connection.close()

        date = pyswing.constants.pySwingStartDate
        if dateString:
            date = datetime.datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")

        return date