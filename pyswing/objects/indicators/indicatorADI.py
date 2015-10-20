import logging
import datetime
import sqlite3

from pandas.io.sql import read_sql_query
from talib import abstract

from utils.Logger import Logger
import pyswing.constants


class IndicatorADI(object):
    """
    Advance Decline Indicator.
    """

    def __init__(self):
        """
        Class Constructor.
        """

        tableName = "Indicator_ADI"

        self._insertQuery = "insert or replace into %s (Date, ADI, ADI_ROC, ADI_EMA, ADI_SUM) values (?,?,?,?,?)" % (tableName)
        self._selectQuery = "SELECT Date, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) - SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) as ADI FROM Equities group by Date"

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        self._indicatorDataFrame = read_sql_query(self._selectQuery, connection, 'Date')

        self._indicatorDataFrame['ADI'] = self._indicatorDataFrame['ADI'].astype(float)

        self._indicatorDataFrame['ADI_ROC'] = abstract.ROC(self._indicatorDataFrame, timeperiod=5, price='ADI')
        self._indicatorDataFrame['ADI_EMA'] = abstract.EMA(self._indicatorDataFrame, timeperiod=5, price='ADI')
        self._indicatorDataFrame['ADI_SUM'] = abstract.SUM(self._indicatorDataFrame, price='ADI')

        self._tableName = "Indicator_ADI"


    def updateIndicator(self):
        """
        Calculate and Store the (New) Indicator Data.
        """

        start = self._getLatestDate()

        Logger.log(logging.INFO, "Updating Indicator", {"scope":__name__, "indicator":self._tableName, "start":str(start)})

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        newRecords = self._indicatorDataFrame.query("Date > '%s'" % (str(start)))

        connection.executemany(self._insertQuery, newRecords.to_records(index=True))

        connection.commit()

        connection.close()


    def _getLatestDate(self):

        connection = sqlite3.connect(pyswing.constants.pySwingDatabase)

        query = "select max(Date) from %s" % (self._tableName)

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