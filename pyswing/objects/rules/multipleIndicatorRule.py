import logging
import sqlite3

from pandas.io.sql import read_sql_query

from pyswing.objects.rules.rule import Rule
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database


class MultipleIndicatorRule(Rule):
    """
    Multiple Indicator Rule Class.
    """

    def __init__(self, indicatorTable1, indicatorTable2, indicatorRule):
        """
        Class Constructor.

        :param ?
        :param ?
        :param indicatorRule: Columns should be prefixed with t1 and t2
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        ruleTableName = "Rule %s %s %s" % (indicatorTable1, indicatorTable2, indicatorRule)
        Rule.__init__(self, ruleTableName)

        self._selectQuery = "select t1.Date, t1.Code, %s as Match from %s t1 inner join %s t2 on t1.Date = t2.Date and t1.Code = t2.Code" % (indicatorRule, indicatorTable1, indicatorTable2)


    def evaluateRule(self, tickerCode):
        """
        ?.
        """

        self._tickerCode = tickerCode
        start = self._getLatestDate()

        Logger.log(logging.INFO, "Evaluating Rule", {"scope":__name__, "Rule":self._ruleTableName, "code":self._tickerCode, "start":str(start)})

        self._restrictedSelectQuery = "%s where t1.Code = '%s' and t1.Date > '%s'" % (self._selectQuery, self._tickerCode, start)

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)

        self._ruleData = read_sql_query(self._restrictedSelectQuery, connection, 'Date')

        self._ruleData['Match'] = self._ruleData['Match'].astype(float)

        connection.executemany(self._insertQuery, self._ruleData.to_records(index=True))
        connection.commit()

        connection.close()