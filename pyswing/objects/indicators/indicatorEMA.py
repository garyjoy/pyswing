from talib import abstract

from pyswing.objects.indicators.indicator import Indicator


class IndicatorEMA(Indicator):
    """
    EMA Indicator(s).
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the EMA-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_EMA"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, EMA_5, EMA_10, EMA_15, EMA_20, EMA_50, EMA_200) values (?,?,?,?,?,?,?,?)" % (tableName)

        equityDataFrame = equityDataFrame

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['EMA_5'] = abstract.EMA(equityDataFrame, timeperiod=5, price='Close')
        indicatorDataFrame['EMA_10'] = abstract.EMA(equityDataFrame, timeperiod=10, price='Close')
        indicatorDataFrame['EMA_15'] = abstract.EMA(equityDataFrame, timeperiod=15, price='Close')
        indicatorDataFrame['EMA_20'] = abstract.EMA(equityDataFrame, timeperiod=20, price='Close')
        indicatorDataFrame['EMA_50'] = abstract.EMA(equityDataFrame, timeperiod=50, price='Close')
        indicatorDataFrame['EMA_200'] = abstract.EMA(equityDataFrame, timeperiod=200, price='Close')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)