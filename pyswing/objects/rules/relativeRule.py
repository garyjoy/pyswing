import logging
import sqlite3
from enum import Enum

from pandas.io.sql import read_sql_query

from pyswing.objects.rules.rule import Rule
from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database


class Comparison(Enum):
    GreaterThan = 1
    LessThan = 2


class RelativeRule(Rule):
    """
    Relative Rule Class.
    """

    def __init__(self, indicatorTable, indicatorColumn, relativeIndex, comparison, multiplier=1.00):
        """
        Class Constructor.

        :param indicatorTable:
        :param indicatorColumn:
        :param relativeIndex: Relative Index to compare the Indicator Column e.g. -1 means previous day and -5 means five days ago
        :param comparison:
        :param multiplier:
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        ruleTableName = "Rule %s %s %s %s %s" % (indicatorTable, indicatorColumn, relativeIndex, comparison, multiplier)
        Rule.__init__(self, ruleTableName)

        self._selectQuery = "select Date, Code, %s from %s" % (indicatorColumn, indicatorTable)

        self._indicatorColumn = indicatorColumn
        self._relativeIndex = relativeIndex
        self._comparison = comparison
        self._multiplier = multiplier


    def evaluateRule(self, tickerCode):
        """
        ?

        :param tickerCode:
        """

        self._tickerCode = tickerCode

        start = self._getLatestDate()

        Logger.log(logging.INFO, "Evaluating Rule", {"scope":__name__, "Rule":self._ruleTableName, "code":self._tickerCode, "start":str(start)})

        # We can't use self._getLatestDate() because we need data from before that date...
        self._restrictedSelectQuery = "%s where Code = '%s'" % (self._selectQuery, self._tickerCode)

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)

        self._ruleData = read_sql_query(self._restrictedSelectQuery, connection, 'Date')

        self._ruleData['Relative'] = self._ruleData[self._indicatorColumn].shift(self._relativeIndex * -1)

        if self._comparison == Comparison.GreaterThan :
            self._ruleData['Match'] = self._ruleData[self._indicatorColumn] > self._multiplier * self._ruleData['Relative']
        else:
            self._ruleData['Match'] = self._ruleData[self._indicatorColumn] < self._multiplier * self._ruleData['Relative']

        self._ruleData['Match'] = self._ruleData['Match'].astype(float)

        self._ruleData.drop('Relative', axis=1, inplace=True)
        self._ruleData.drop(self._indicatorColumn, axis=1, inplace=True)

        newRecords = self._ruleData.query("Date > '%s'" % (str(start)))

        connection.executemany(self._insertQuery, newRecords.to_records(index=True))
        connection.commit()

        connection.close()