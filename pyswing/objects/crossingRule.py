import logging
import datetime
import sqlite3

from pandas.io.sql import read_sql_query
from pyswing.objects.rule import Rule

from utils.Logger import Logger
import pyswing.constants

from enum import Enum


class Comparison(Enum):
    GreaterThan = 1
    LessThan = 2


class CrossingRule(Rule):
    """
    Crossing Rule Class.
    """

    def __init__(self, crosserTable, crosserColumn, crosseeTable, crosseeColumn):
        """
        Class Constructor.

        :param crosserTable:
        :param crosserColumn:
        :param crosseeTable:
        :param crosseeColumn:
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        ruleTableName = "Rule %s %s Cross %s %s" % (crosserTable, crosserColumn, crosseeTable, crosseeColumn)
        Rule.__init__(self, ruleTableName)

        if crosserTable == crosseeTable:
            self._selectQuery = "select r.Date, r.Code, %s as Crosser, %s as Crossee from %s r" % (crosserColumn, crosseeColumn, crosserTable)
        else:
            self._selectQuery = "select r.Date, r.Code, r.%s as Crosser, e.%s as Crossee from %s r inner join %s e on r.Date = e.Date and r.Code = e.Code" % (crosserColumn, crosseeColumn, crosserTable, crosseeTable)

        self._crosserColumn = crosserColumn
        self._crosseeColumn = crosseeColumn


    def evaluateRule(self, tickerCode):
        """
        ?

        :param tickerCode:
        """

        self._tickerCode = tickerCode

        start = self._getLatestDate()

        Logger.log(logging.INFO, "Evaluating Rule", {"scope":__name__, "Rule":self._ruleTableName, "code":self._tickerCode, "start":str(start)})

        self._restrictedSelectQuery = "%s where r.Code = '%s' and r.Date >= '%s'" % (self._selectQuery, self._tickerCode, start)

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        self._ruleData = read_sql_query(self._restrictedSelectQuery, connection, 'Date')

        self._ruleData['LastCrosser'] = self._ruleData['Crosser'].shift(1)
        self._ruleData['LastCrossee'] = self._ruleData['Crossee'].shift(1)

        self._ruleData['Match'] = (self._ruleData['Crosser'] > self._ruleData['Crossee']) & (self._ruleData['LastCrossee'] > self._ruleData['LastCrosser'])

        self._ruleData['Match'] = self._ruleData['Match'].astype(float)

        self._ruleData.drop('Crosser', axis=1, inplace=True)
        self._ruleData.drop('Crossee', axis=1, inplace=True)
        self._ruleData.drop('LastCrosser', axis=1, inplace=True)
        self._ruleData.drop('LastCrossee', axis=1, inplace=True)

        newRecords = self._ruleData.query("Date > '%s'" % (str(start)))

        connection.executemany(self._insertQuery, newRecords.to_records(index=True))
        connection.commit()

        connection.close()