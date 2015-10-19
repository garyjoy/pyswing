from talib import abstract

from pyswing.objects.indicators.indicator import Indicator


class IndicatorAROON(Indicator):
    """
    Aroon Indicator(s).
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Aroon-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_AROON"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, AROON_DOWN, AROON_UP, Code) values (?,?,?,?)" % (tableName)

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame = abstract.AROON(equityDataFrame, timeperiod=14, prices=['High', 'Low'])
        indicatorDataFrame['Code'] = tickerCode

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)