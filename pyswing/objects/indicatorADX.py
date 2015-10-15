from talib import abstract

from pyswing.objects.indicator import Indicator


class IndicatorADX(Indicator):
    """
    Average Directional Indicator(s).

    14 Day
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Average Directional-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_ADX"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, ADX, ADX_ROC) values (?,?,?,?)" % (tableName)

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['ADX'] = abstract.ADX(equityDataFrame, timeperiod=14, prices=['High', 'Low', 'Close'])
        indicatorDataFrame['ADX_ROC'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='ADX')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)