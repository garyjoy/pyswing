from talib import abstract

from pyswing.objects.indicators.indicator import Indicator


class IndicatorBB20(Indicator):
    """
    Bollinger Band Indicator(s).

    20 Day SMA with 2x Standard Deviations
    """

    def __init__(self, equityDataFrame, tickerCode):
        """
        Create the Bollinger Band-specific logic. Everything else lives in the Indicator Base Class.

        :param equityDataFrame: A Pandas DataFrame from the Equity Class.
        :param tickerCode: Ticker Code (String).
        """

        tableName = "Indicator_BB20"
        tickerCode = tickerCode

        insertQuery = "insert or replace into %s (Date, upperband, middleband, lowerband, Code, upperbandroc, middlebandroc, lowerbandroc) values (?,?,?,?,?,?,?,?)" % (tableName)

        equityDataFrame = equityDataFrame

        # Stick the Indicator Values into the new DataFrame
        indicatorDataFrame = abstract.BBANDS(equityDataFrame, 20, 2, 2, price='Close')
        indicatorDataFrame['Code'] = tickerCode
        indicatorDataFrame['upperbandroc'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='upperband')
        indicatorDataFrame['middlebandroc'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='middleband')
        indicatorDataFrame['lowerbandroc'] = abstract.ROC(indicatorDataFrame, timeperiod=5, price='lowerband')

        Indicator.__init__(self, tableName, tickerCode, insertQuery, equityDataFrame, indicatorDataFrame)