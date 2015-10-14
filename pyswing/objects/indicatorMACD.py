from talib import abstract

from pyswing.objects.indicator import Indicator


class IndicatorMACD(Indicator):
    """
    MACD Indicator(s).
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the MACD-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_MACD"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, MACD_12_26, MACD_12_26_9, MACD_12_26_9_DIVERGENCE) values (?,?,?,?,?)" % (tableName)

        equityDataFrame = equityDataFrame

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame = abstract.MACD(equityDataFrame, fastperiod=12, slowperiod=26, signalperiod=9, price='Close')
        indicatorDataFrame['Code'] = tickerCode

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)