import logging
import datetime
import sqlite3

from pandas.io.sql import read_sql_query
from pyswing.objects.rule import Rule

from utils.Logger import Logger
import pyswing.constants


class SimpleRule(Rule):
    """
    Simple Rule Class.
    """

    def __init__(self, indicatorTable, indicatorRule):
        """
        Class Constructor.

        :param ?
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        ruleTableName = "Rule %s %s" % (indicatorTable, indicatorRule)
        Rule.__init__(self, ruleTableName)

        self._insertQuery = "insert or replace into '%s' (Date, Code, Match) values (?,?,?)" % (self._ruleTableName)

        self._selectQuery = "select Date, Code, %s from %s as Match" % (indicatorRule, indicatorTable)


    def evaluateRule(self, tickerCode):
        """
        ?.
        """

        self._tickerCode = tickerCode
        start = self._getLatestDate()

        Logger.log(logging.INFO, "Evaluating Rule", {"scope":__name__, "Rule":self._ruleTableName, "code":self._tickerCode, "start":str(start)})

        self._restrictedSelectQuery = "%s where Code = '%s' and Date > '%s'" % (self._selectQuery, self._tickerCode, start)

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        self._ruleData = read_sql_query(self._restrictedSelectQuery, connection, 'Date')

        connection.executemany(self._insertQuery, self._ruleData.to_records(index=True))
        connection.commit()

        connection.close()


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