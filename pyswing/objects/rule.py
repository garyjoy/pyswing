import logging
import datetime
import sqlite3

from utils.Logger import Logger
import pyswing.constants


def getRules():

    connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

    query = "SELECT name FROM sqlite_master WHERE type = 'table' and name like 'Rule %'"

    rules = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rules = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Rules", {"scope":__name__})

    connection.close()

    return [(rule[0]) for rule in rules]


class Rule(object):
    """
    Rule Base Class.
    """

    CreateTableCommand = "CREATE TABLE IF NOT EXISTS '%s' (Date TEXT, Code TEXT, Match INT, PRIMARY KEY (Date, Code));"
    CreateDateIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_Date' ON '%s' (Date);"
    CreateCodeIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_Code' ON '%s' (Code);"

    def __init__(self, ruleTableName):
        """
        Base Class Constructor.

        :param ?
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        self._ruleTableName = ruleTableName
        self._createTable()

        self._insertQuery = "insert or replace into '%s' (Date, Code, Match) values (?,?,?)" % (self._ruleTableName)


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

    def _createTable(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        c = connection.cursor()
        c.executescript(Rule.CreateTableCommand % (self._ruleTableName))
        c.executescript(Rule.CreateDateIndexCommand % (self._ruleTableName, self._ruleTableName))
        c.executescript(Rule.CreateCodeIndexCommand % (self._ruleTableName, self._ruleTableName))
        connection.commit()
        c.close()
        connection.close()