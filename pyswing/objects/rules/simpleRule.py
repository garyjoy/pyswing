import logging
import sqlite3

from pandas.io.sql import read_sql_query

from pyswing.objects.rules.rule import Rule
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database


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

        self._selectQuery = "select Date, Code, %s as Match from %s" % (indicatorRule, indicatorTable)


    def evaluateRule(self, tickerCode):
        """
        ?.
        """

        self._tickerCode = tickerCode
        start = self._getLatestDate()

        Logger.log(logging.INFO, "Evaluating Rule", {"scope":__name__, "Rule":self._ruleTableName, "code":self._tickerCode, "start":str(start)})

        self._restrictedSelectQuery = "%s where Code = '%s' and Date > '%s'" % (self._selectQuery, self._tickerCode, start)

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)

        self._ruleData = read_sql_query(self._restrictedSelectQuery, connection, 'Date')

        self._ruleData['Match'] = self._ruleData['Match'].astype(float)

        connection.executemany(self._insertQuery, self._ruleData.to_records(index=True))
        connection.commit()

        connection.close()