import datetime
import logging
import sqlite3

from pandas.io.data import DataReader
from pandas.io.sql import read_sql_query

from utils.Logger import Logger
import pyswing.constants


class Equity(object):
    """
    An Equity object provides an interface to Share Price Data for a specified Ticker Code.

    It uses pandas (DataReader and DataFrame) and SQLite as a local data store.

    Use importData() to update the SQLite data from Yahoo (adjusting as necessary) and use dataFrame() to get at the
    adjusted data.
    """

    def __init__(self, tickerCode):
        """
        Constructor.

        There isn't much to see here. It just makes a note of the Ticker Code.

        :param tickerCode: Ticker Code.
        """

        Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({tickerCode})})

        self._tickerCode = tickerCode


    def importData(self):
        """
        Import (New) Data from Yahoo.
        """

        start = self._getLatestDate()
        end = self._getTodaysDate()

        Logger.log(logging.INFO, "Loading Data", {"scope":__name__, "tickerCode":self._tickerCode, "start":str(start), "end":str(end)})
        self._data = DataReader(self._tickerCode, "yahoo", start, end)

        self._data['Code'] = self._tickerCode

        for item in ['Open', 'High', 'Low']:
            self._data[item] = self._data[item] * self._data['Adj Close'] / self._data['Close']

        self._data.drop('Close', axis=1, inplace=True)
        self._data.rename(columns={'Adj Close':'Close'}, inplace=True)
        self._data['Volume'] = self._data['Volume'].astype(float)

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = "insert or replace into Equities (Date, Open, High, Low, Volume, Close, Code) values (?,?,?,?,?,?,?)"
        connection.executemany(query, self._data.to_records(index=True))
        connection.commit()

        connection.close()

    def dataFrame(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)
        query = "select * from Equities where Code = '%s'" % (self._tickerCode)
        equityData = read_sql_query(query, connection, 'Date')
        connection.close()

        return equityData


    def _getLatestDate(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = "select max(Date) from Equities where Code = '%s'" % (self._tickerCode)

        cursor = connection.cursor()

        cursor.execute(query)
        dateString = cursor.fetchone()[0]

        connection.close()

        date = pyswing.constants.pySwingStartDate
        if dateString:
            date = datetime.datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")

        return date

    def _getTodaysDate(self):

        return datetime.datetime.now()