from talib import abstract

from pyswing.objects.indicators.indicator import Indicator


class IndicatorROC(Indicator):
    """
    Rate of Change Indicator(s).
    """

    tableName = "Indicator_ROC"

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Rate of Change-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, Code, ROC_5, ROC_10, ROC_20) values (?,?,?,?,?)" % (IndicatorROC.tableName)

        equityDataFrame = equityDataFrame

        # Create a new DataFrame with just Date and Code
        indicatorDataFrame = equityDataFrame.ix[:,'Code':]

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame['ROC_5'] = abstract.ROC(equityDataFrame, timeperiod=5, price='Close')
        indicatorDataFrame['ROC_10'] = abstract.ROC(equityDataFrame, timeperiod=10, price='Close')
        indicatorDataFrame['ROC_20'] = abstract.ROC(equityDataFrame, timeperiod=20, price='Close')

        Indicator.__init__(self, IndicatorROC.tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)