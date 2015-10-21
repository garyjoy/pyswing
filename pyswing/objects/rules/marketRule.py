import logging
import sqlite3
import datetime


from pandas.io.sql import read_sql_query

from pyswing.objects.rules.rule import Rule
from utils.Logger import Logger
import pyswing.constants
from pyswing.objects.rules.relativeRule import Comparison


class MarketRule(object):
    """
    Market Rule Class.
    """

    CreateTableCommand = "CREATE TABLE IF NOT EXISTS '%s' (Date TEXT, Match INT, PRIMARY KEY (Date));"
    CreateDateIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_Date' ON '%s' (Date);"

    def __init__(self, indicatorTable, indicatorColumn, relativeIndex, comparison, multiplier=1.00):
        """
        Class Constructor.

        :param ?
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        self._ruleTableName = "Rule %s %s %s %s %s" % (indicatorTable, indicatorColumn, relativeIndex, comparison, multiplier)

        self._createTable()

        self._insertQuery = "insert or replace into '%s' (Date, Match) values (?,?)" % (self._ruleTableName)

        self._selectQuery = "select Date, %s from %s" % (indicatorColumn, indicatorTable)

        self._indicatorColumn = indicatorColumn
        self._relativeIndex = relativeIndex
        self._comparison = comparison
        self._multiplier = multiplier


    def evaluateRule(self):
        """
        ?

        :param tickerCode:
        """

        start = self._getLatestDate()

        Logger.log(logging.INFO, "Evaluating Rule", {"scope":__name__, "Rule":self._ruleTableName, "start":str(start)})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        self._ruleData = read_sql_query(self._selectQuery, connection, 'Date')

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

    def analyseRule(self):
        """
        ?
        """

        Logger.log(logging.INFO, "Analysing Rule", {"scope":__name__, "Rule":self._ruleTableName})

        potentialRuleMatches = self._getPotentialRuleMatches()

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        cursor = connection.cursor()

        try:
            query = "select count(1) from '%s' where Match = 1;" % self._ruleTableName
            cursor.execute(query)
            actualRuleMatches = int(cursor.fetchone()[0])

            query = "delete from Rules where Rule = '%s'" % self._ruleTableName
            cursor.execute(query)

            # Unit Testing is easier if the value is stored...
            self._matchesPerDay = actualRuleMatches / potentialRuleMatches
            query = "insert into Rules values('%s',%s)" % (self._ruleTableName, self._matchesPerDay)
            cursor.execute(query)

        except sqlite3.OperationalError:
            Logger.log(logging.INFO, "Error Analysing Rule", {"scope":__name__, "Rule":self._ruleTableName})

        connection.commit()

        connection.close()


    def _getLatestDate(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = "select max(Date) from '%s'" % (self._ruleTableName)

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

    def _createTable(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(Rule.CreateTableCommand % (self._ruleTableName))
        c.executescript(Rule.CreateDateIndexCommand % (self._ruleTableName, self._ruleTableName))
        connection.commit()
        c.close()
        connection.close()

    def _getPotentialRuleMatches(self):

        if not pyswing.globals.potentialRuleMatches:

            connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

            query = "select count(1) from '%s'" % self._ruleTableName

            cursor = connection.cursor()

            try:
                cursor.execute(query)
                pyswing.globals.potentialRuleMatches = int(cursor.fetchone()[0])
            except sqlite3.OperationalError:
                Logger.log(logging.INFO, "Error Getting Potential Rule Matches", {"scope":__name__, "rule":self._ruleTableName})

            connection.close()

        return pyswing.globals.potentialRuleMatches
