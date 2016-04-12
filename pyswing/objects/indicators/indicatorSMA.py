from talib import abstract

from pyswing.objects.indicators.indicator import Indicator


class IndicatorSMA(Indicator):
    """
    SMA Indicator(s).
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the SMA-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_SMA"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, SMA_5, SMA_10, SMA_15, SMA_20, SMA_50, SMA_100, SMA_200, SMA_300) values (?,?,?,?,?,?,?,?,?,?)" % (tableName)

        equityDataFrame = equityDataFrame

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['SMA_5'] = abstract.SMA(equityDataFrame, timeperiod=5, price='Close')
        indicatorDataFrame['SMA_10'] = abstract.SMA(equityDataFrame, timeperiod=10, price='Close')
        indicatorDataFrame['SMA_15'] = abstract.SMA(equityDataFrame, timeperiod=15, price='Close')
        indicatorDataFrame['SMA_20'] = abstract.SMA(equityDataFrame, timeperiod=20, price='Close')
        indicatorDataFrame['SMA_50'] = abstract.SMA(equityDataFrame, timeperiod=50, price='Close')
        indicatorDataFrame['SMA_100'] = abstract.SMA(equityDataFrame, timeperiod=100, price='Close')
        indicatorDataFrame['SMA_200'] = abstract.SMA(equityDataFrame, timeperiod=200, price='Close')
        indicatorDataFrame['SMA_300'] = abstract.SMA(equityDataFrame, timeperiod=300, price='Close')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)