from talib import abstract

from pyswing.objects.indicators.indicator import Indicator


class IndicatorRSI(Indicator):
    """
    Relative Strength Indicator(s).

    14 Day
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Relative Strength-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_RSI"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, RSI) values (?,?,?)" % (tableName)

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['RSI'] = abstract.RSI(equityDataFrame, timeperiod=14, price='Close')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)