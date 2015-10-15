from talib import abstract

from pyswing.objects.indicator import Indicator


class IndicatorDX(Indicator):
    """
    Directional Indicator(s).

    14 Day
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Directional-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_DX"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, DX, DX_ROC) values (?,?,?,?)" % (tableName)

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['DX'] = abstract.DX(equityDataFrame, timeperiod=14, prices=['High', 'Low', 'Close'])
        indicatorDataFrame['DX_ROC'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='DX')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)