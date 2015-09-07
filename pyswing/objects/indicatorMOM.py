from talib import abstract

from pyswing.objects.indicator import Indicator


class IndicatorMOM(Indicator):
    """
    Momentum Indicator(s).
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Momentum-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_MOM"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, MOM_5, MOM_10, MOM_20) values (?,?,?,?,?)" % (tableName)

        equityDataFrame = equityDataFrame

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['MOM_5'] = abstract.MOM(equityDataFrame, timeperiod=5, price='Close')
        indicatorDataFrame['MOM_10'] = abstract.MOM(equityDataFrame, timeperiod=10, price='Close')
        indicatorDataFrame['MOM_20'] = abstract.MOM(equityDataFrame, timeperiod=20, price='Close')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)