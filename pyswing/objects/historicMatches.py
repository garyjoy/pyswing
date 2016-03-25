import logging
import sqlite3

from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database


class HistoricMatches(object):
    """
    ?
    """

    def __init__(self):
        """
        ?
        """

        Logger.log(logging.DEBUG, "Log Object Creation", {"scope": __name__})

        self._rules = self._getRules()

    def createTable(self):

        self._createTable(0, 50)
        self._createTable(51, 100)
        self._createTable(101, 150)
        self._createTable(151, 200)

        deleteTableStatement = "DROP TABLE IF EXISTS HistoricMatches"
        createTableStatement = """CREATE TABLE HistoricMatches AS
                                    select h1.Date, h1.Code, h1.matchString || h2.matchString || h3.matchString || h4.matchString as matchString
                                    from HistoricMatches_0_50 h1
                                    inner join HistoricMatches_51_100 h2 on h1.Date = h2.Date and h1.Code = h2.Code
                                    inner join HistoricMatches_101_150 h3 on h1.Date = h3.Date and h1.Code = h3.Code
                                    inner join HistoricMatches_151_200 h4 on h1.Date = h4.Date and h1.Code = h4.Code
                                    """

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        c = connection.cursor()
        c.executescript(deleteTableStatement)
        c.executescript(createTableStatement)
        connection.commit()
        c.close()
        connection.close()

    def _createTable(self, startIndex, stopIndex):

        Logger.log(logging.INFO, "Create Historic Matches Table",
                   {"scope": __name__, "startIndex": str(startIndex), "stopIndex": str(stopIndex)})

        deleteTableStatement, createTableStatement = self._generateSqlStatements(startIndex, stopIndex)

        # print(deleteTableStatement)
        # print(createTableStatement)

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        c = connection.cursor()
        c.executescript(deleteTableStatement)
        c.executescript(createTableStatement)
        connection.commit()
        c.close()
        connection.close()

    def _getRules(self):
        connection = sqlite3.connect(pyswing.database.pySwingDatabase)

        query = "SELECT name FROM sqlite_master WHERE type='table' and name like 'Rule %' order by name"

        rules = None

        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rules = cursor.fetchall()
        except sqlite3.OperationalError:
            Logger.log(logging.INFO, "Error Getting Rules", {"scope": __name__})

        connection.close()

        return [(rule[0]) for rule in rules]

    def _generateSqlStatements(self, startIndex, stopIndex):

        tableName = "HistoricMatches_%i_%i" % (startIndex, stopIndex)

        deleteTableStatement = "DROP TABLE IF EXISTS %s" % (tableName)

        createTableStatement = "CREATE TABLE %s AS \n" % (tableName)
        selectStatement = "select r%i.Date, r%i.Code, ''" % (startIndex, startIndex)
        fromStatement = ""
        joinStatement = ""

        for index, rule in enumerate(self._rules):

            if index >= startIndex and index <= stopIndex:

                selectStatement += " || ifnull(r%i.Match, 0)" % (index)

                if index == startIndex:
                    fromStatement = "\nfrom \"%s\" r%i\n" % (rule, index)
                else:
                    if "_ADI" in rule:
                        joinStatement += "inner join \"%s\" r%i on r%i.Date = r%i.Date\n" % (
                        rule, index, startIndex, index)
                    else:
                        joinStatement += "inner join \"%s\" r%i on r%i.Date = r%i.Date and r%i.Code = r%i.Code\n" % (
                        rule, index, startIndex, index, startIndex, index)

        selectStatement += " as matchString"

        createTableStatement += selectStatement + fromStatement + joinStatement

        return (deleteTableStatement, createTableStatement)
