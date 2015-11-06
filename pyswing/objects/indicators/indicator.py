import logging
import datetime
import sqlite3

from pyswing.utils.Logger import Logger
import pyswing.constants


class Indicator(object):
    """
    Indicator Base Class.
    """

    def __init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame):
        """
        Base Class Constructor.

        :param tableName: Table Name
        :param tickerCode: Ticker Code
        :param insertQuery: Insert Query (see updateIndicator())
        :param equityDataFrame: Equity Data (from Equity Object)
        :param indicatorDataFrame: Indicator Data (calculated in Child Class Constructor)
        """

        # Logger.log(logging.DEBUG, "Log Object Creation", {"scope":__name__, "arguments":" ".join({""})})

        self._tableName = tableName
        self._tickerCode = tickerCode

        self._insertQuery = insertQuery

        self._equityDataFrame = equityDataFrame
        self._indicatorDataFrame = indicatorDataFrame


    def updateIndicator(self):
        """
        Calculate and Store the (New) Indicator Data.
        """

        start = self._getLatestDate()

        Logger.log(logging.INFO, "Updating Indicator", {"scope":__name__, "indicator":self._tableName, "code":self._tickerCode, "start":str(start)})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        newRecords = self._indicatorDataFrame.query("Date > '%s'" % (str(start)))

        connection.executemany(self._insertQuery, newRecords.to_records(index=True))

        connection.commit()

        connection.close()


    def _getLatestDate(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = "select max(Date) from %s where Code = '%s'" % (self._tableName, self._tickerCode)

        cursor = connection.cursor()

        dateString = None
        try:
            cursor.execute(query)
            dateString = cursor.fetchone()[0]
        except sqlite3.OperationalError:
            Logger.log(logging.INFO, "Table Does Not Exist", {"scope":__name__, "table":self._tableName})

        connection.close()

        date = pyswing.constants.pySwingStartDate
        if dateString:
            date = datetime.datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")

        return date