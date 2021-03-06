import logging
import sqlite3

from pandas.io.sql import read_sql_query

from pyswing.utils.Logger import Logger
import pyswing.constants
import pyswing.database


def getExitStrategies():

    connection = sqlite3.connect(pyswing.database.pySwingDatabase)

    query = "SELECT name FROM sqlite_master WHERE type = 'table' and name like 'Exit %'"

    exitStrategies = None

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        exitStrategies = cursor.fetchall()
    except sqlite3.OperationalError:
        Logger.log(logging.INFO, "Error Getting Exit Strategies", {"scope":__name__})

    connection.close()

    return [(exitStrategy[0]) for exitStrategy in exitStrategies]


class ExitValues(object):
    """
    Exit Values Base Class.
    """

    CreateTableCommand = "CREATE TABLE IF NOT EXISTS '%s' (Date TEXT, Code TEXT, Type TEXT, ExitValue REAL, NumberOfDays INT, ExitDetail TEXT, MatchDate TEXT, PRIMARY KEY (MatchDate, Code, Type));"
    CreateDateIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_Date' ON '%s' (Date);"
    CreateMatchDateIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_MatchDate' ON '%s' (MatchDate);"
    CreateCodeIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_Code' ON '%s' (Code);"
    CreateTypeIndexCommand = "CREATE INDEX IF NOT EXISTS 'ix_%s_Type' ON '%s' (Type);"


    def __init__(self, tickerCode):
        """
        Base Class Constructor.

        :param tableName: Table Name
        :param tickerCode: Ticker Code
        :param equityDataFrame: Equity Data (from Equity Object)
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        self._createTable()
        self._tickerCode = tickerCode
        self._buyExitValueDataFrame = None
        self._sellExitValueDataFrame = None
        self._insertQuery = "insert or replace into '%s' (Date, Code, Type, ExitValue, NumberOfDays, ExitDetail, MatchDate) values (?,?,?,?,?,?,?)" % (self._tableName)


    def calculateExitValues(self):

        Logger.log(logging.INFO, "Calculating Exit Values", {"scope":__name__, "Rule":self._tableName, "code":self._tickerCode})

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)

        self._selectBuyQuery = "select e.Date as Date, e.Date as TradeDate, e.Code, e.Open, e.Close, e.High, e.Low, x.Type, x.ExitValue, x.NumberOfDays, x.ExitDetail from Equities e left join '%s' x on e.Date = x.MatchDate and e.Code = x.Code and x.Type = 'Buy' where e.Code = '%s' and x.ExitValue is NULL" % (self._tableName, self._tickerCode)
        self._buyExitValueDataFrame = read_sql_query(self._selectBuyQuery, connection, "Date")

        numberOfRows = self._buyExitValueDataFrame.shape[0]
        for i in range(0, numberOfRows):
            self.calculateExitValueForBuy(i, numberOfRows - i)

        self._buyExitValueDataFrame.drop('Open', axis=1, inplace=True)
        self._buyExitValueDataFrame.drop('Close', axis=1, inplace=True)
        self._buyExitValueDataFrame.drop('High', axis=1, inplace=True)
        self._buyExitValueDataFrame.drop('Low', axis=1, inplace=True)
        self._buyExitValueDataFrame['MatchDate'] = self._buyExitValueDataFrame['TradeDate'].shift(1)
        self._buyExitValueDataFrame.drop('TradeDate', axis=1, inplace=True)

        newRecords = self._buyExitValueDataFrame.query("Type=='Buy'")
        connection.executemany(self._insertQuery, newRecords.to_records(index=True))
        connection.commit()

        self._selectSellQuery = "select e.Date as Date, e.Date as TradeDate, e.Code, e.Open, e.Close, e.High, e.Low, x.Type, x.ExitValue, x.NumberOfDays, x.ExitDetail from Equities e left join '%s' x on e.Date = x.MatchDate and e.Code = x.Code and x.Type = 'Sell' where e.Code = '%s' and x.ExitValue is NULL" % (self._tableName, self._tickerCode)
        self._sellExitValueDataFrame = read_sql_query(self._selectSellQuery, connection, "Date")

        numberOfRows = self._sellExitValueDataFrame.shape[0]
        for i in range(0, numberOfRows):
            self.calculateExitValueForSell(i, numberOfRows - i)

        self._sellExitValueDataFrame.drop('Open', axis=1, inplace=True)
        self._sellExitValueDataFrame.drop('Close', axis=1, inplace=True)
        self._sellExitValueDataFrame.drop('High', axis=1, inplace=True)
        self._sellExitValueDataFrame.drop('Low', axis=1, inplace=True)
        self._sellExitValueDataFrame['MatchDate'] = self._sellExitValueDataFrame['TradeDate'].shift(1)
        self._sellExitValueDataFrame.drop('TradeDate', axis=1, inplace=True)

        newRecords = self._sellExitValueDataFrame.query("Type=='Sell'")
        connection.executemany(self._insertQuery, newRecords.to_records(index=True))
        connection.commit()

        connection.close()

    def calculateExitValueForBuy(self, rowIndex, numberOfRows):
        """
        ?
        """

        raise NotImplementedError("")

    def calculateExitValueForSell(self, rowIndex, numberOfRows):
        """
        ?
        """

        raise NotImplementedError("")


    def _createTable(self):

        connection = sqlite3.connect(pyswing.database.pySwingDatabase)
        c = connection.cursor()
        c.executescript(ExitValues.CreateTableCommand % (self._tableName))
        c.executescript(ExitValues.CreateDateIndexCommand % (self._tableName, self._tableName))
        c.executescript(ExitValues.CreateMatchDateIndexCommand % (self._tableName, self._tableName))
        c.executescript(ExitValues.CreateCodeIndexCommand % (self._tableName, self._tableName))
        c.executescript(ExitValues.CreateTypeIndexCommand % (self._tableName, self._tableName))
        connection.commit()
        c.close()
        connection.close()